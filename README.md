# badgerDAPS
A Brute Ratel LDAP query-log sorting tool, for the aspiring anti-LDAP query/Windows powershell hacker.
## Summary
Maybe you hate running specific LDAP queries or drilling down into BR LDAP data. Filtering by OU and running multiple queries can be painstakingly tedious, not to mention the opposite of opsec-safe. If you're trying to get the queries correct but you find yourself making filtering mistakes, resulting in probably one too many LDAP commands sent to the beacon, this tool is meant to help you. In addition, with the BR LDAP output, you're going to have to remove brackets, spaces, etc, just to be able to use hostnames with other tooling. It's difficult to filter this data without coming up with custom sed or awk syntax, or trying to use the BR output with powershell just to pull the hostnames, and get all of them in a new line file. Simply put, this tool enhances your workflow to help you quickly grab hosts by OU from LDAP Sentinel queries. You can then use the sorted output files with CrackMapExec, SharpShares, etc. badgerDAPS natively removes disabled hosts too, which is useful for ensuring that you're not accidentally trying to interact with disabled machines on the network - which is undoubtedly a red flag that might burn your entire operation (so is pulling all objects with LDAP but we wont discuss that) -- spoiler alert, we will.

QUICK NOTE: The logs that you filter from must:
- Be output from Brute Ratel's LDAP functionality
- At a minimum, contain the sAMAccountName, memberOf and AccountDisabled fields. If you don't have these fields in your BR LDAP queries, this tool will not function properly. 
## Example Usage
Let's say you goofed up and didn't filter by specific OU, and you ran this beautiful command that will return all computer objects from the company active directory:
```
sentinel domain (&(objectCategory=computer)(objectClass=computer)name=*)
```
Well, the output is going to be extensive. It might look something like this:
```
+-------------------------------------------------------------------+
[+] objectClass                        : top; person; organizationalPerson; user; computer
[+] displayName                        : EXAMPLE-HOST-1$
[+] uSNCreated                         : 
[+] memberOf                           : CN=EXAMPLE1,OU=Application Permissions,OU=EVILCORP Groups,DC=EVILCORP,DC=com
[+] uSNChanged                         : 
[+] name                               : EXAMPLE-HOST-1
[+] objectGUID                         : {.......}
[+] userAccountControl                 : 4096
[+] codePage                           : 0
[+] countryCode                        : 0
[+] lastLogon                          : 5/26/2020 3:47:35 PM
[+] localPolicyFlags                   : 0
[+] pwdLastSet                         : 9/13/2021 7:01:41 AM
[+] primaryGroupID                     : 515
[+] objectSid                          : ..........
[+] accountExpires                     : Never expires
[+] sAMAccountName                     : EXAMPLE-HOST-1$
[+] sAMAccountType                     : 805306369
[+] operatingSystem                    : Windows 10 Enterprise
[+] operatingSystemVersion             : 10.0 (19042)
[+] dNSHostName                        : EXAMPLE-HOST-1.EVILCORP.com
[+] servicePrincipalName               : WSMAN/EXAMPLE-HOST-1.EVILCORP.com; TERMSRV/EXAMPLE-HOST-1.EVILCORP.com; RestrictedKrbHost/EXAMPLE-HOST-1.EVILCORP.com; HOST/EXAMPLE-HOST-1.EVILCORP.com; WSMAN/EXAMPLE-HOST-1.EVILCORP.com; TERMSRV/EXAMPLE-HOST-1.EVILCORP.com; RestrictedKrbHost/EXAMPLE-HOST-1.EVILCORP.com; HOST/EXAMPLE-HOST-1.EVILCORP.com
[+] ADsPath                            : LDAP://CN=EXAMPLE-HOST-1.EVILCORP.com,OU=Workstations,OU=EVILCORP Computers,DC=EVILCORP,DC=com
[+] PasswordExpiry                     : 01-01-1970 00:0
[+] AccountDisabled                    : FALSE

+-------------------------------------------------------------------+
```
Even if you filtered by OU properly, or apply other sorting options, you'll still likely get output that looks similar to the one above, and this tool can be utilized efficiently if you have the required fields described in the tool summary.

Utilizing baderDAPS is simple, this is how you filter by specific OU:
```
└─$ python3 badgerDAPS.py 

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
    
Please enter the file name or file path: b-20.log
Disabled accounts have been removed.

Would you like to filter by OU? (Y/N)
Y
1. Computers
2. Domain Controllers
3. Incident Response Servers
4. Servers

Enter an OU number, or press 'x' to exit.
4

Filtering complete. 217 results have been written to Servers.txt

Enter an OU number, or press 'x' to exit.
```
As you can see, seperate OU files can be created. The end result is a neatly formatted, newline host file that can be passed to other red team tools.
```
└─$ cat Servers.txt 
SERVER-1-FOO
SERVER-2-FOO
SERVER-3-FOO
.....
```
Lastly, maybe you intentionally ran a giant LDAP query, and you don't want a small sorted host list by OU, but instead, want a list of all enabled host machines on the network. badgerDAPS can do that for you.
```
Please enter the file name or file path: b-20.log
Disabled accounts have been removed.

Would you like to filter by OU? (Y/N)
N

Filtering complete. 857 results have been written to all-results.txt
```
## FAQ
- Why go through all of this and not just use LDAP options properly to grab hostnames of non-disabled machines, if that's what you ultimately want?
  You'll still have spacing, brackets, and a non-formatted list. Even if you filter and drill down to what you want, you'll still have to work at it to get a newline list. Sometimes when I'm operating, I just want to quickly move onto taking some hostnames for specific OUs and passing it to CME or SharpShares. This mitigates at least a certain level of work associated.

- I can do this better. Why don't you just use: (insert some windows ldap filtering method utilizing some estoric python package that i've never heard of)
  Then do it better. No one is stopping you. This method works for me, and might help some other people too.
