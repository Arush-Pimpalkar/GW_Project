import pycbc.noise
from pycbc.noise import noise_from_psd
import pycbc.psd
import pylab as plt
import csv
from pycbc.waveform import get_td_waveform
import random
import numpy as np
from pycbc.types import TimeSeries, Array


T = 4
flow = 30.0
delta_f = 1.0 / T
flen = int(2048 / delta_f) + 1
delta_t = 1.0 / 4096
tsamples = int(T / delta_t)

scale = 1200


# PSD
psd = pycbc.psd.aLIGOZeroDetHighPower(flen, delta_f, flow)
noisesamples = int(4 / delta_t)


with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_train.csv",
    "w",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["M1", "M2", "Time", "SNR", "Path"])


def get_shifted_wvfrm(shift_percent):
    # WVFRM generation
    global hp, m1, m2
    m1 = random.randint(10, 30)
    m2 = random.randint(10, 30)

    print(m1, m2)
    hp, hc = get_td_waveform(
        approximant="IMRPhenomT",
        mass1=m1,
        mass2=m2,
        delta_t=1.0 / 4096,
        f_lower=30,
    )
    hp.resize(16384)
    hc.resize(16384)

    # Shift the waveform
    total_length = len(hp.sample_times)
    shift_index = int(shift_percent * total_length)
    shifted_data = np.zeros_like(hp.data)
    shift_amount = min(len(hp.data), total_length - shift_index)
    shifted_data[shift_index : shift_index + shift_amount] = hp.data[:shift_amount]
    ts = TimeSeries(shifted_data, delta_t=delta_t)
    return ts, m1, m2, hp


def get_noise(seed):
    noise = noise_from_psd(tsamples, delta_t, psd, seed=seed)
    return noise


def get_time_and_snr(template, signal):

    snr = pycbc.filter.matched_filter(
        template, signal, psd=psd, low_frequency_cutoff=flow
    )

    peak = abs(snr).numpy().argmax()
    snrp = abs(snr[peak])
    time = snr.sample_times[peak]

    return time, snrp


with open(
    "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_train.csv",
    "w",
    newline="",
) as file:
    writer = csv.writer(file)
    writer.writerow(["M1", "M2", "Time", "SNR", "Path"])


def save_func(index, csv_parameters_batch, waveforms):
    with open(
        "/home/arush/GW_Project_1/Data_Generation/Continous_Check/cont_data_train.csv",
        "a",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerows(csv_parameters_batch)

    for i, waveform in enumerate(waveforms):
        plt.specgram(waveform, Fs=2048)
        plt.axis("off")
        plt.savefig(
            f"/home/arush/GW_Project_1/Data_Generation/Continous_Check/Data/signal_{index + i}.png",
            bbox_inches="tight",
            pad_inches=0,
        )
        plt.close()


l = 0
batch_size = 10
batch_data = []
waveforms = []


while l < 100:
    random_shift_var = random.uniform(0, 0.7)

    waveform, m1, m2, template = get_shifted_wvfrm(random_shift_var)
    noise = get_noise(l)

    signal = (waveform / scale) + noise
    # plt.specgram(signal, Fs=2048)
    plt.show()
    time, snr = get_time_and_snr(template=template, signal=signal)

    chirp_m = ((m1 * m2) ** (3 / 5)) / ((m1 + m2) ** (1 / 5))

    csv_append = [m1, m2, time, snr, chirp_m]
    batch_data.append(csv_append)

    # Save in batches to minimize I/O operations
    if l % batch_size == 0 and l != 0:
        save_func(l, batch_data, np.array(signal))
        batch_data = []  # Reset batch data to free memory

    l += 1
