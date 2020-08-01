import os
import json
from pathlib import Path


def json_write(data, fname) -> bool:
    """
    Write to JSON file given data.
    """
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


def allen_break_json() -> bool:
    """
    Load OOS data from DATA_DIR into a Dict of pd.DataFrames.

    :param all: Whether to load 'all_wiki_sents.txt' as well.
    :return data: Dictionary containing CLINC data as dataframes.
    """
    data_dir = Path(os.getenv("DATA_DIR"))
    oos_data_dir = data_dir/"oos-eval/data/"
    files = next(os.walk(oos_data_dir))[2]
    data = {}
    print(f"Loading files: {files!r}")

    paths = {f[:f.find('.')]:oos_data_dir/f for f in files}

    print(paths)

    for filen, path in paths.items():
        with open(path, "r") as data_f:
            ext = str(path)[-5:]
            begin = str(filen)[:4]

            if ext == ".json":
                data_f_json = json.load(data_f)
            else:
                continue
                # TODO Add the bit for all here.

            print(data_f_json.keys())
            train_data = {
                "train": data_f_json["train"]
            }
            val_data = {
                "val": data_f_json["val"]
            }
            test_data = {
                "test": data_f_json["test"]
            }

            if begin == "data":
                train_data["train"] += data_f_json["oos_train"]
                val_data["val"] += data_f_json["oos_val"]
                test_data["test"] += data_f_json["oos_test"]

            json_write(train_data, filen + "_train.json")
            json_write(val_data, filen + "_val.json")
            json_write(test_data, filen + "_test.json")


    return True


allen_break_json()
