from bs4 import BeautifulSoup


def read_table(path):
    with open(path, "rb") as f:
        html = BeautifulSoup(f, "html.parser")
    return html("table")[-1]

def get_headers(table):
    return [th.text.strip() for th in table.thead("th")]

def get_data(table):
    body = table.tbody("tr")

    same = [""] * 5
    idx = 0
    records = []

    for row in body:
        cols = row("th")
        rest = []
        colspan = False

        for th in cols:
            if th.has_attr("rowspan"):
                same[idx] = th.text.strip()
                if "level-4" not in th["class"]:
                    idx += 1
            elif th.has_attr("colspan"):
                idx -= 1
                colspan = True
                break
            else:
                rest.append(th.text.strip())

        if colspan:
            continue

        rest += [td.text.strip() for td in row("td")]

        assert len(same) + len(rest) == 12

        records.append(";".join(same + rest))
    
    return records
        

def main():
    table = read_table("../HTML/model_per_year.html")
    header = get_headers(table)

    with open("../DataSets/[RAW]model_per_year.csv", "w") as f:
        f.write(";".join(header) + "\n")
        f.writelines([record + "\n" for record in get_data(table)])

if __name__ == "__main__":
    print("Executing Scraping_Model_Per_Year.py")
    main()

