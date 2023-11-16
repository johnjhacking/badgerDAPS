# --BADGERDAPS--
# Created by John Jackson
#########################
# For filtering your Brute Ratel LDAP queries like a caveman
import os

def print_red_ascii_art(art):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(RED + art + RESET)

def remove_disabled_accounts(file_path, ou_filter=None):
    with open(file_path, 'r') as file:
        content = file.read()

    entries = content.split('+-------------------------------------------------------------------+')
    enabled_accounts = [entry for entry in entries if 'AccountDisabled                    : FALSE' in entry]

    ous = set()
    for entry in enabled_accounts:
        lines = entry.split('\n')
        for line in lines:
            if line.startswith('[+] distinguishedName'):
                parts = line.split(',')
                for part in parts:
                    if part.strip().startswith('OU='):
                        ous.add(part.split('=')[1].strip())

    print("Disabled accounts have been removed.")
    return enabled_accounts, sorted(list(ous))

def write_results(ou_filter, enabled_accounts, remove_dollar_sign=False):
    if ou_filter:
        filtered_accounts = [entry for entry in enabled_accounts if ou_filter in entry]
    else:
        filtered_accounts = enabled_accounts

    cns = []
    for account in filtered_accounts:
        lines = account.split('\n')
        for line in lines:
            if line.startswith('[+] sAMAccountName'):
                cn = line.split(':')[1].strip()
                if remove_dollar_sign:
                    cn = cn.replace('$', '')
                cns.append(cn)

    return cns

def main():
    ascii_art = r"""
             ___,,___
           _,-='=- =-  -`"--.__,,.._
        ,-;// /  - -       -   -= - "=.
      ,'///    -     -   -   =  - ==-=\`.
     |/// /  =    `. - =   == - =.=_,,._ `=/|
    ///    -   -    \  - - = ,ndDMHHMM/\b  \\
  ,' - / /        / /\ =  - /MM(,,._`YQMML  `|
 <_,=^Kkm / / / / ///H|wnWWdMKKK#""-;. `"0\  |
        `""QkmmmmmnWMMM\""WHMKKMM\   `--. \> \
 hjm          `""'  `->>>    ``WHMb,.    `-_<@)
                                `"QMM`.
                                   `>>>
    Badger does what badger wants.
    """
    print_red_ascii_art(ascii_art)

    file_path = input("Please enter the file name or file path: ")
    if not os.path.exists(file_path):
        print("The file does not exist. Please check the path and try again.")
        return

    enabled_accounts, ous = remove_disabled_accounts(file_path)

    print("\nWould you like to filter by OU? (Y/N)")
    filter_choice = input().strip().upper()
    ou_filter = None
    if filter_choice == 'Y':
        for i, ou in enumerate(ous, start=1):
            print(f"{i}. {ou}")

        while True:
            print("\nEnter an OU number, or press 'x' to exit.")
            choice = input().strip()
            if choice.lower() == 'x':
                break
            if choice.isdigit() and 1 <= int(choice) <= len(ous):
                ou_filter = ous[int(choice)-1]
                output_file = f"{ou_filter}.txt"
                results = write_results(ou_filter, enabled_accounts, remove_dollar_sign=True)
                with open(output_file, 'w') as f:
                    for cn in results:
                        f.write(cn + '\n')
                print(f"\nFiltering complete. {len(results)} results have been written to {output_file}")

    elif filter_choice == 'N':
        output_file_name = "all-results.txt"
        results = write_results(None, enabled_accounts, remove_dollar_sign=True)
        with open(output_file_name, 'w') as f:
            for cn in results:
                f.write(cn + '\n')
        print(f"\nFiltering complete. {len(results)} results have been written to {output_file_name}")

if __name__ == "__main__":
    main()
