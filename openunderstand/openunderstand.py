import os.path
from os import path, getcwd
import argparse
import configparser


def save_config(
    repo_address: str, db_address: str, db_name: str, engine_core: str, log_address: str
) -> None:
    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "repo_address": repo_address,
        "db_address": db_address,
        "db_name": db_name,
        "engine_address": engine_core,
    }
    config["Logging"] = {"filename": log_address, "level": "DEBUG"}

    if os.path.isfile("config.ini"):
        existing_config = configparser.ConfigParser()
        existing_config.read("config.ini")

        for section in config.sections():
            for attr, value in config[section].items():
                if value is not None and attr in existing_config[section]:
                    existing_config[section][attr] = value

        with open("config.ini", "w") as configfile:
            existing_config.write(configfile)
            configfile.close()
    else:
        with open("config.ini", "w") as configfile:
            config.write(configfile)
            configfile.close()


def parse_arguments() -> None:
    parser = argparse.ArgumentParser(
        description="CLI for setting configuration options"
    )
    parser.add_argument(
        "-r", "--repo_address", type=str, help="Repository address of project"
    )
    parser.add_argument(
        "-dba", "--db_address", type=str, help="Database SQLite address"
    )
    parser.add_argument("-dbn", "--db_name", type=str, help="Database SQLite name file")
    parser.add_argument(
        "-e",
        "--engine_core",
        type=str,
        help="Engine for parser usage (C++ or Python)",
    )
    parser.add_argument(
        "-l", "--log_address", type=str, help="App log name address file"
    )
    args = parser.parse_args()
    repo_address = (
        args.repo_address if args.repo_address else path.join(getcwd(), "project")
    )
    db_address = args.db_address if args.db_address else path.join(getcwd())
    db_name = args.db_name if args.db_name else "default.oudb"
    engine_core = args.engine_core if args.engine_core else "Python"
    log_address = (
        args.log_address if args.log_address else path.join(getcwd(), "app.log")
    )
    save_config(
        repo_address=repo_address,
        db_address=db_address,
        db_name=db_name,
        engine_core=engine_core,
        log_address=log_address,
    )


def start_parsing(
    repo_address: str = None,
    db_address: str = None,
    db_name: str = None,
    engine_core: str = None,
    log_address: str = None,
):
    from oudb.api import create_db
    from oudb.fill import fill
    from ounderstand.runner import runner

    if (
        repo_address is not None
        and db_address is not None
        and db_name is not None
        and engine_core is not None
        and log_address is not None
    ):
        save_config(
            repo_address=repo_address,
            db_address=db_address,
            db_name=db_name,
            engine_core=engine_core,
            log_address=log_address,
        )
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
    except :
        raise Exception("please init all input values of start_parsing() function or run command line cli openunderstand \n - >> this error occur because of config.ini not exist")
    create_db(
        dbname=config["DEFAULT"]["db_name"],
        project_dir=config["DEFAULT"]["repo_address"],
        db_path=config["DEFAULT"]["db_address"],
    )
    fill(udb_path=config["DEFAULT"]["db_address"])
    runner(path_project=config["DEFAULT"]["repo_address"])


if __name__ == "__main__":
    parse_arguments()
    start_parsing()
