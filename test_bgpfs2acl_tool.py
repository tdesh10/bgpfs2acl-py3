import pytest

from bgpfs2acl import BgpFs2AclTool

DEFAULT_ACL_NAME = 'bgpfs2acl-test'


class TestBgpFs2AclTool:
    @pytest.mark.parametrize(
        ('test_input', 'expected'),
        [
            (  # Case 1: mixed
                    {
                        'interface Loopback0': [
                            'ipv4 address 11.11.11.11 255.255.255.255',
                        ],
                        'interface MgmtEth0/RP0/CPU0/0': [
                            'ipv4 address 10.30.111.177 255.255.255.224',
                            'lldp',
                            'enable',
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                        'interface TenGigE0/0/0/0': [
                            'shutdown',
                        ],
                        'interface TenGigE0/0/0/1': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                        'interface TenGigE0/0/0/2': [
                            'shutdown',
                        ],
                        'interface TenGigE0/0/0/3': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ]
                    },
                    {
                        'interface MgmtEth0/RP0/CPU0/0': [
                            'ipv4 address 10.30.111.177 255.255.255.224',
                            'lldp',
                            'enable',
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                        'interface TenGigE0/0/0/1': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                        'interface TenGigE0/0/0/3': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ]
                    }
            ),
            (  # Case 2: no acl
                    {
                        'interface Loopback0': [
                            'ipv4 address 11.11.11.11 255.255.255.255',
                        ],
                        'interface TenGigE0/0/0/0': [
                            'shutdown',
                        ],
                        'interface TenGigE0/0/0/2': [
                            'shutdown',
                        ],
                    },
                    {}
            ),
            (  # Case 3: only acl
                    {
                        'interface TenGigE0/0/0/1': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                    },
                    {
                        'interface TenGigE0/0/0/1': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                    }
            ),
            (  # Case 4: empty interface list
                    {},
                    {}
            )
        ]
    )
    def test_get_interfaces_by_acl_name(self, test_input, expected):
        interfaces_list = test_input
        fs_start_seq = 100500
        tool = BgpFs2AclTool()
        result = tool.get_interfaces_by_acl_name(interfaces_list, DEFAULT_ACL_NAME)

        assert result == expected

    @pytest.mark.parametrize(
        ('test_input', 'expected', 'with_shutdown'),
        [
            (  # Case 1: mixed
                    '''interface MgmtEth0/RP0/CPU0/0
ipv4 address 10.30.111.177 255.255.255.224
lldp
enable
!
!
interface TenGigE0/0/0/0
shutdown
!
interface TenGigE0/0/0/1
shutdown
ipv4 access-group bgpfs2acl-test ingress
!
interface TenGigE0/0/0/2
ipv4 access-group bgpfs2acl-test ingress
shutdown
!
interface TenGigE0/0/0/11
ipv4 access-group bgpfs2acl-test ingress
!'''.split('\n'),
                    {
                        'interface MgmtEth0/RP0/CPU0/0': [
                            'ipv4 address 10.30.111.177 255.255.255.224',
                            'lldp',
                            'enable',
                        ],
                        'interface TenGigE0/0/0/0': [
                            'shutdown',
                        ],
                        'interface TenGigE0/0/0/1': [
                            'shutdown',
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ],
                        'interface TenGigE0/0/0/2': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                            'shutdown',
                        ],
                        'interface TenGigE0/0/0/11': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ]
                    },
                    True
            ),
            (  # Case 2: with shutdown in input, no shutdown in output
                    '''interface MgmtEth0/RP0/CPU0/0
ipv4 address 10.30.111.177 255.255.255.224
lldp
enable
!
!
interface TenGigE0/0/0/2
ipv4 access-group bgpfs2acl-test ingress
shutdown
!
interface TenGigE0/0/0/3
shutdown
ipv4 access-group bgpfs2acl-test ingress
!
interface TenGigE0/0/0/11
ipv4 access-group bgpfs2acl-test ingress
!'''.split('\n'),
                    {
                        'interface MgmtEth0/RP0/CPU0/0': [
                            'ipv4 address 10.30.111.177 255.255.255.224',
                            'lldp',
                            'enable',
                        ],
                        'interface TenGigE0/0/0/11': [
                            'ipv4 access-group bgpfs2acl-test ingress',
                        ]
                    },
                    False
            ),
            (  # Case 3: only with shutdown
                    '''interface TenGigE0/0/0/2
ipv4 access-group bgpfs2acl-test ingress
shutdown
!
interface TenGigE0/0/0/3
shutdown
ipv4 access-group bgpfs2acl-test ingress
!
interface TenGigE0/0/0/11
shutdown
ipv4 access-group bgpfs2acl-test ingress
!'''.split('\n'),
                    {},
                    False
            ),
            (  # Case 4: empty interface list
                    {},
                    {},
                    True
            )
        ]
    )
    def test_get_interfaces(self, test_input, expected, with_shutdown):
        tool = BgpFs2AclTool()
        result = tool.get_interfaces(test_input, with_shutdown)

        assert result == expected


    
    