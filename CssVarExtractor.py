def extract(css, wars):
    extracted_vars = []

    if '$' in css:
        pos = css.index('$')
        for i in range(pos + 1, len(css)):
            if css[pos+1:i+1] in wars:
                extracted_vars.append(css[pos+1:i+1])

    return extracted_vars


if __name__ == "__main__":
    css = "background: $cpt"

    wars = {
        "cpt": "hello"
    }

    print(extract(css,wars))