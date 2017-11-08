import sys
import imaplib
import getpass
import email
import collections

import re
imaplib._MAXLINE = 400000



def process_mailbox(M, prefix="addresses", max_tuples=10000, account=""):
    
    pat = "<[\w_.-]+@[\w_.-]+>"

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    adressees = set()
    total = len(data[0].split())

    for i, num in enumerate(data[0].split()):
        try:
            rv, data = M.fetch(num, '(RFC822)')
        except:
            rv = "error"
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        to  = str(msg["To"])

        ms = re.finditer(pat, to)
        tos = sorted([m.group().lower().replace("<", "").replace(">", "") for m in ms])
        tos = tuple(tos)
        adressees.add(tos)

        if len(adressees) > max_tuples:
            break

        sys.stdout.write("%d/%d (%d)\r" % (i, total, len(adressees)))
        sys.stdout.flush()

    fp = open("%s.txt" % prefix, "w")
    for addr in adressees:
        fp.write("%s\n" % "\t".join(sorted(addr)))
    fp.close()
    print("File %s.txt generated." % prefix)


def generate_files(prefix="addresses", min_tuple_length=1, max_tuple_length=15):

    people = collections.defaultdict(int)
    links  = collections.defaultdict(int)

    for addresses in open("%s.txt" % prefix, "rt"):
        addrs = []
        for addr in addresses.strip().split("\t") :
            if "@" not in addr:
                continue
            addrs.append(addr.lower())

        if max_tuple_length > len(addrs) > min_tuple_length:
            for i, p1 in enumerate(addrs):
                people[p1] += 1
                for p2 in addrs[:i]:
                    links[min(p1, p2), max(p1, p2)] += 1

        add_d = dict((a, i+1) for i, a in enumerate(people))

    f = open("%s.net" % prefix, "wt")
    f.write('*Network "no name" \n\n')
    f.write("*Vertices\t%i\n" % len(people))
    f.write("\n".join('\t%i\t"%s"' % (add_d[p], p.encode("utf8")) for p in people))
    f.write("\n*Edges\n")
    f.write("".join("\t%i\t%i\t%i\n" % (add_d[a1], add_d[a2], w) for (a1, a2), w in links.items()))
    f.close()
    print("File %s.net generated." % prefix)

    f = open("%s.tab" % prefix, "wt")
    f.write("ime\tmailov\n")
    f.write("s\tc\n")
    f.write("meta\t\n")
    f.write("\n".join("%s\t%i" % (n.encode("utf8"), m) for n, m in people.items()))
    f.close()
    print("File %s.tab generated." % prefix)




def generate_addressee_network(email_address, imap='imap.gmail.com', max_tuples=1000,
                              email_folder="INBOX", file_prefix="addresses",
                              min_tuple_length=2, max_tuple_length=15):
    """
    
    Generate files of addresee network of a given IMAP email inbox.
    
    The following files are generated:
        <file_prefix>.txt (Tuples containing common addresees).
        <file_prefix>.tab (Properties of nodes: number of emails)
        <file_prefix>.net (Network file in pajek format)

    :param email_address: Account address.
    :param imap: Imap server (default='imap.gmail.com')
    :param email_folder: Mailbox folder (default='INBOX')
    :param file_prefix: File prefix (default="addresses")
    :param max_tuples: Maximum number of addressee tuples to be read (default=1000)
    :param min_tuple_length: Store only emails with at minumum number of adressees (defalut=2)
    """                         


    M = imaplib.IMAP4_SSL(imap)

    try:
        print("Account: %s" % email_address)
        rv, data = M.login(email_address, getpass.getpass())
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED")
        sys.exit(1)

    rv, data = M.select(email_folder)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M, max_tuples=max_tuples, prefix=file_prefix, account=email_address)
        generate_files(prefix=file_prefix, min_tuple_length=min_tuple_length, max_tuple_length=max_tuple_length)


        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)

    M.logout()




if __name__ == "__main__":
    import sys
    myself = sys.argv[1] if len(sys.argv) else "someone@gmail.com"
    generate_addressee_network(myself)