import unittest
from falafel.mappers.nfnetlink_queue import NfnetLinkQueue
from falafel.tests import context_wrap


NFNETLINK_QUEUE = """
    0  -4423     0 2 65535     0     0       22  1
    1  -4424     0 2 65535     0     0       27  1
    2  -4425     0 2 65535     0     0       17  1
    3  -4426     0 2 65535     0     0       14  1
    4  -4427     0 2 65535     0     0       22  1
    5  -4428     0 2 65535     0     0       16  1
""".strip()

CORRUPT_NFNETLINK_QUEUE_1 = """
    0  -4423     0 2 65535     0     0       22  1
    1  -4424     0 2 6553
    2  -4425     0 2 65535     0     0       17  1
    3  -4426     0 2 65535     0     0       14  1
    4  -4427     0 2 65535     0     0       22  1
    5  -4428     0 2 65535     0     0       16  1
""".strip()

CORRUPT_NFNETLINK_QUEUE_2 = """
    0  -4423     0 2 65535     0     0       22  1
    1  -4424     0 2 astring   0     0       27  1
    2  -4425     0 2 65535     0     0       17  1
    3  -4426     0 2 65535     0     0       14  1
    4  -4427     0 2 65535     0     0       22  1
    5  -4428     0 2 65535     0     0       16  1
""".strip()


class TestNfnetLinkQueue(unittest.TestCase):

    def test_parse_content(self):
        nfnet_link_queue = NfnetLinkQueue(context_wrap(NFNETLINK_QUEUE))
        row = nfnet_link_queue.data[0]
        self.assertEquals(row["queue_number"], 0)
        self.assertEquals(row["peer_portid"], -4423)
        self.assertEquals(row["queue_total"], 0)
        self.assertEquals(row["copy_mode"], 2)
        self.assertEquals(row["copy_range"], 65535)
        self.assertEquals(row["queue_dropped"], 0)
        self.assertEquals(row["user_dropped"], 0)
        self.assertEquals(row["id_sequence"], 22)

        row = nfnet_link_queue.data[5]
        self.assertEquals(row["queue_number"], 5)
        self.assertEquals(row["peer_portid"], -4428)
        self.assertEquals(row["queue_total"], 0)
        self.assertEquals(row["copy_mode"], 2)
        self.assertEquals(row["copy_range"], 65535)
        self.assertEquals(row["queue_dropped"], 0)
        self.assertEquals(row["user_dropped"], 0)
        self.assertEquals(row["id_sequence"], 16)

    def test_missing_columns(self):
        self.assertRaises(AssertionError, NfnetLinkQueue, context_wrap(CORRUPT_NFNETLINK_QUEUE_1))

    def test_wrong_type(self):
        self.assertRaises(ValueError, NfnetLinkQueue, context_wrap(CORRUPT_NFNETLINK_QUEUE_2))
        pass