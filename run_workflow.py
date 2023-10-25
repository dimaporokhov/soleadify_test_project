from workflow import raw, transform, process


def run_workflow():
    print("RUNNING RAW PART")
    raw.main()

    print("\nRUNNING TRANSFORM PART")
    transform.main()

    print("\nRUNNING PROCESS PART")
    process.main()


if __name__ == '__main__':
    run_workflow()
