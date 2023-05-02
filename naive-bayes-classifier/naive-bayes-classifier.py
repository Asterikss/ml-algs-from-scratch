import pathlib
import logging

def ask_for_data_loc() -> pathlib.Path: # ~~pure
    while True:
        answer = int(input("For default data location type 1. Otherwise type 0: "))
        if answer == 1:
            return pathlib.Path("data/" + "iris_training.txt")
        elif answer == 0:
            while True:
                custom_path = pathlib.Path((input("Enter custom data location")))
                if custom_path.exists():
                    return custom_path
                print("Path not found")


def downlad_dataset(data_loc: pathlib.Path) -> tuple[list[list[float]], int, list[str], list[int], list[list[float]]]: # pure
    collected_data = []
    label_tabel = []
    # ^, v - not using a dict since indexes matter
    label_occurrence_tabel = []

    #           [
    # feature_n   [min, max]
    # feature_n+1 [min, max]
    # ...
    #                      ]
    min_and_max_table: list[list[float]] = []
    firstTime = True
    

    with open(data_loc, "r", encoding="utf-8") as f:
        for line in f:
            splited: list[str] = line.split()
            if firstTime:
                    min_and_max_table: list[list[float]] = [[0,0] for _ in range(len(splited) - 1)]
            
            decoded: list[float] = []
            for i in range(len(splited) - 1):
                tmp_eval = eval(splited[i])
                decoded.append(tmp_eval)

                if firstTime:
                    min_and_max_table[i][0] = tmp_eval
                    min_and_max_table[i][1] = tmp_eval
                

                if not firstTime:
                    if tmp_eval < min_and_max_table[i][0]:
                        min_and_max_table[i][0] = tmp_eval
                    elif tmp_eval > min_and_max_table[i][1]:
                        min_and_max_table[i][1] = tmp_eval

            firstTime = False



            label = splited[-1]
            if label not in label_tabel:
                label_tabel.append(label)
                label_occurrence_tabel.append(0)

            index = label_tabel.index(label)
            decoded.append(index)
            label_occurrence_tabel[index] += 1
            
            collected_data.append(decoded)

    number_of_feature = len(collected_data[0]) - 1
    logging.info(f"Number of features: {number_of_feature}")
    logging.info(f"Label table: {label_tabel}")
    logging.info(f"Label occurrence table: {label_occurrence_tabel}")
    logging.info(f"Length of the dataset: {len(collected_data)}")
    logging.info(f"min and max table: {min_and_max_table}")

    return collected_data, number_of_feature, label_tabel, label_occurrence_tabel, min_and_max_table


def calc_prior_prob(label_occurrence_tabel: list[int], n_of_examples: int) -> list[float]: # pure
    prior_prob = []
    for n_of_given_label in label_occurrence_tabel:
        prior_prob.append(n_of_given_label / n_of_examples)

    logging.info(f"Prior probabilities : {prior_prob}")
    return prior_prob


def train():
    ...

def bin_dataset(dataset: list[list[float]], min_and_max_table: list[list[float]], n_bins=3) -> list[list[float]]: # pure
    binned_dataset: list[list[float]] = []
    print(binned_dataset)

    intervals_len: list[float] = [round((min_and_max_table[i][1] - min_and_max_table[i][0]) / n_bins, 2) for i in range(len(min_and_max_table))]
    logging.info(f"Intervals length: {intervals_len}")
    
    bins: list[list[list[float]]] = []

    for j in range(len(min_and_max_table)):
        bins.append([[min_and_max_table[j][0] + (intervals_len[j] * i), min_and_max_table[j][0] + (intervals_len[j] * (i + 1))] for i in range(n_bins)])

    logging.info(f"Bins: {bins}")

    # Allocate each feature in each example in the dataset to its bean (replace it with the index of the bin that it lies in for the given feature).
    # Seperate bins are created for every feature. Number of bins = n_bins * n_features
    for example in dataset:
        tmp_binned_example = []
        for i in range(len(example) - 1):
            allocated_to_bin_index = -1
            for j in range(n_bins):
                if example[i] >= bins[i][j][0] and example[i] <= bins[i][j][1]:
                    allocated_to_bin_index = j

            tmp_binned_example.append(allocated_to_bin_index)

        tmp_binned_example.append(example[-1])
        binned_dataset.append(tmp_binned_example)


    print(dataset)
    print("--------------")
    print(binned_dataset)

    return binned_dataset
    # for example in dataset:
    #     pass




def init():
    level = logging.INFO
    # level = logging.DEBUG
    fmt = "%(levelname)s:%(lineno)d:%(funcName)s: %(message)s"
    logging.basicConfig(level = level, format = fmt) # filename = 'log_x.log', filemode = "w"


def main():
    init()
    data_loc: pathlib.Path = ask_for_data_loc()
    dataset, number_of_feature, label_tabel, label_occurrence_tabel, min_and_max_table = downlad_dataset(data_loc)
    prior_probability: list[float] = calc_prior_prob(label_occurrence_tabel, len(dataset))
    binned_dataset = bin_dataset(dataset, min_and_max_table)


if __name__ == "__main__":
    main()
