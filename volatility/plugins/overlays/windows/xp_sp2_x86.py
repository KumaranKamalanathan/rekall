# Volatility
# Copyright (c) 2008 Volatile Systems
# Copyright (c) 2008 Brendan Dolan-Gavitt <bdolangavitt@wesleyan.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. 
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#

"""
@author:       Brendan Dolan-Gavitt
@license:      GNU General Public License 2.0 or later
@contact:      bdolangavitt@wesleyan.edu

This file provides support for windows XP SP2. We provide a profile
for SP2.
"""

#pylint: disable-msg=C0111

import windows
import xp_sp2_x86_vtypes
import xp_sp2_x86_syscalls
import crash_vtypes
import hibernate_vtypes
import kdbg_vtypes
import tcpip_vtypes
import volatility.debug as debug #pylint: disable-msg=W0611

# These are updates applied to the autogenerated vtypes. In particulat
# they are types that are not defined in the autogenerated set.

xp_sp2_x86_vtypes.nt_types.update(crash_vtypes.crash_vtypes)
xp_sp2_x86_vtypes.nt_types.update(hibernate_vtypes.hibernate_vtypes)
xp_sp2_x86_vtypes.nt_types.update(kdbg_vtypes.kdbg_vtypes)
xp_sp2_x86_vtypes.nt_types.update(tcpip_vtypes.tcpip_vtypes)

# Standard vtypes are usually autogenerated by scanning through header
# files, collecting debugging symbol data etc. This file defines
# fixups and improvements to the standard types.
xpsp2overlays = {
    'VOLATILITY_MAGIC' : [None, {
    # Profile specific values
    'DTBSignature' : [ 0x0, ['VolatilityMagic', dict(value = "\x03\x00\x1b\x00")]],
    'KUSER_SHARED_DATA' : [ 0x0, ['VolatilityMagic', dict(value = 0xFFDF0000)]],
    'KDBGHeader' : [ 0x0, ['VolatilityMagic', dict(value = '\x00\x00\x00\x00\x00\x00\x00\x00KDBG\x90\x02')]],
    # Configuration options
    'DTB' : [ 0x0, ['VolatilityDTB', dict(configname = "DTB")]],
    'KPCR' : [ 0x0, ['VolatilityMagic', dict(value = 0xffdff000, configname = "KPCR")]],
    'KDBG' : [ 0x0, ['VolatilityKDBG', dict(configname = "KDBG")]],
    'IA32ValidAS': [ 0x0, ['VolatilityIA32ValidAS']],
    # Pool allocations are aligned to this many bytes.
    'PoolAlignment': [0x0, ['VolatilityMagic', dict(value = 8)]],
    }],

    '_EPROCESS' : [ None, {
    'CreateTime' : [ None, ['WinTimeStamp', {}]],
    'ExitTime' : [ None, ['WinTimeStamp', {}]],
    'InheritedFromUniqueProcessId' : [ None, ['unsigned int']],
    'ImageFileName' : [ None, ['String', dict(length = 16)]],
    'UniqueProcessId' : [ None, ['unsigned int']],
    'VadRoot': [ None, ['pointer', ['_MMVAD']]],
    }],

    '_ETHREAD' : [ None, {
    'CreateTime' : [ None, ['ThreadCreateTimeStamp', {}]],
    'ExitTime' : [ None, ['WinTimeStamp', {}]],
    }],

    '_OBJECT_SYMBOLIC_LINK' : [ None, {
    'CreationTime' : [ None, ['WinTimeStamp', {}]],
    }],

    '_KUSER_SHARED_DATA' : [ None, {
    'SystemTime' : [ None, ['WinTimeStamp', {}]],
    'TimeZoneBias' : [ None, ['WinTimeStamp', {}]],
    }],

    '_KPROCESS' : [ None, {
    'DirectoryTableBase' : [ None, ['unsigned long']],
    }],

    '_KGDTENTRY' : [  None , {
    'BaseMid' : [ 0x4, ['unsigned char']],
    'BaseHigh' : [ 0x7, ['unsigned char']],
    }],

    '_ADDRESS_OBJECT' : [ None, {
    'LocalPort': [ None, ['unsigned be short']],
    'CreateTime' : [ None, ['WinTimeStamp', {}]],
    }],

    '_OBJECT_HEADER' : [ None, {
    'Body' : [ None, ['unsigned int']],
    }],

    '_HANDLE_TABLE_ENTRY' : [ None, {
    'Object' : [ None, ['_EX_FAST_REF']],
    }],

    '_IMAGE_SECTION_HEADER' : [ None, {
    'Name' : [ 0x0, ['String', dict(length = 8)]],
    }],

    '_DBGKD_GET_VERSION64' : [  None, {
    'DebuggerDataList' : [ None, ['pointer', ['unsigned long']]],
    }],

    '_DMP_HEADER' : [ None, {
    'PsActiveProcessHead' : [ None, ['pointer' , ['unsigned long']]],
    }],

    '_CM_KEY_NODE' : [ None, {
    'Signature' : [ None, ['String', dict(length = 2)]],
    'LastWriteTime' : [ None, ['WinTimeStamp', {}]],
    'Name' : [ None, ['String', dict(length = lambda x: x.NameLength)]],
    }],

    '_CM_NAME_CONTROL_BLOCK' : [ None, {
    'Name' : [ None, ['String', dict(length = lambda x: x.NameLength)]],
    }],

    '_CHILD_LIST' : [ None, {
    'List' : [ None, ['pointer', ['array', lambda x: x.Count,
                                 ['pointer', ['_CM_KEY_VALUE']]]]],
    }],

    '_CM_KEY_VALUE' : [ None, {
    'Signature' : [ None, ['String', dict(length = 2)]],
    'Name' : [ None, ['String', dict(length = lambda x: x.NameLength)]],
    }],

    '_CM_KEY_INDEX' : [ None, {
    'Signature' : [ None, ['String', dict(length = 2)]],
    'List' : [ None, ['array', lambda x: x.Count.v() * 2, ['pointer', ['_CM_KEY_NODE']]]],
    }],

    '_IMAGE_HIBER_HEADER' : [ None, {
    'Signature':   [ None, ['String', dict(length = 4)]],
    'SystemTime' : [ None, ['WinTimeStamp', {}]],
    }],

    '_PHYSICAL_MEMORY_DESCRIPTOR' : [ None, {
    'Run' : [ None, ['array', lambda x: x.NumberOfRuns, ['_PHYSICAL_MEMORY_RUN']]],
    }],

    '_TOKEN' : [ None, {
    'UserAndGroupCount' : [ None, ['unsigned long']],
    'UserAndGroups' : [ None, ['pointer', ['array', lambda x: x.UserAndGroupCount,
                                 ['_SID_AND_ATTRIBUTES']]]],
    }],

    '_SID' : [ None, {
    'Revision' : [ None, ['unsigned char']],
    'SubAuthorityCount' : [ None, ['unsigned char']],
    'IdentifierAuthority' : [ None, ['_SID_IDENTIFIER_AUTHORITY']],
    'SubAuthority' : [ None, ['array', lambda x: x.SubAuthorityCount, ['unsigned long']]],
    }],

    '_TCPT_OBJECT': [ None, {
    'RemotePort': [ None, [ 'unsigned be short']],
    'LocalPort': [ None, [ 'unsigned be short']],
    }],

    '_CLIENT_ID': [ None, {
    'UniqueProcess' : [ None, ['unsigned int']],
    'UniqueThread' : [ None, ['unsigned int']],
    }],

    '_MMVAD_SHORT': [ None, {
    # This is the location of the MMVAD type which controls how to parse the
    # node. It is located before the structure.
    'Tag': [-4 , ['String', dict(length = 4)]],
    }],

    '_MMVAD_LONG': [ None, {
    # This is the location of the MMVAD type which controls how to parse the
    # node. It is located before the structure.
    'Tag': [-4 , ['String', dict(length = 4)]],
    }],
}

class WinXPSP2x86(windows.AbstractWindowsX86):
    """ A Profile for Windows XP SP2 """
    _md_major = 5
    _md_minor = 1
    abstract_types = xp_sp2_x86_vtypes.nt_types
    overlay = xpsp2overlays
    syscalls = xp_sp2_x86_syscalls.syscalls
