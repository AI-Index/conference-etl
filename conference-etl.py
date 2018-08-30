import argparse
from subprocess import call


def main(sourcelist):
    print("Running Main Script")
    cmd = ["python", "extract.py"]
    if sourcelist:
        cmd.extend(["--sourcelist", sourcelist])
    call(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Full ETL Pipeline')
    parser.add_argument(
        '--sourcelist',
        help='The filename of sources from which to extract data'
    )
    args = parser.parse_args()
    main(args.sourcelist)
