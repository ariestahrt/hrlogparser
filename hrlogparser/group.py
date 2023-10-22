import pandas as pd

if __name__ == "__main__":
    dataset_list = [
        "casper-rw",
        "dfrws-2009-jhuisi",
        "dfrws-2009-nssal",
        "honeynet-challenge7",
        "honeynet-challenge5",
    ]

    for dataset in dataset_list:
        csv_file = f"../output/{dataset}.csv"

        df = pd.read_csv(csv_file)

        # remove column source
        df = df.drop(columns=['source'])

        # group by "message", then count the number of occurences
        df = df.groupby(['message']).size().reset_index(name='counts')

        # sort by counts
        df = df.sort_values(by=['counts'], ascending=False)

        # save to csv
        df.to_csv(f"../output/{dataset}-grouped.csv", index=False)