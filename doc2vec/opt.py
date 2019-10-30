import argparse

def parse():
    parser = argparse.ArgumentParser(description='Paper Crawler by YLC')
    parser.add_argument('--url', type=str,
                        help='crawl')
    parser.add_argument('--json_data', type=str,
                        default='data/data.json')
    parser.add_argument('--n_class', type=int,
                        default=5)
    parser.add_argument('--topk', type=int,
                        default=5)

    args = parser.parse_args()
    return args
