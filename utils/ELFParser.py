

# Refer: https://linux.die.net/include/elf.h

from ctypes import *
import struct
import io
import sys

# Standard ELF types. #

# Data Type #
# 8-bit c_ubyte c_byte
# 16-bit c_ushort c_short
# 32-bit c_uint c_int
# 64-bit c_ulonglong c_longlong

# Type for a 16-bit quantity. #
Elf32_Half = c_ushort
Elf64_Half = c_ushort

# Types for signed and unsigned 32-bit quantities. #
Elf32_Word  = c_uint
Elf32_Sword = c_int
Elf64_Word  = c_uint
Elf64_Sword = c_int

# Types for signed and unsigned 64-bit quantities. #
Elf32_Xword  = c_ulonglong
Elf32_Sxword = c_longlong
Elf64_Xword  = c_ulonglong
Elf64_Sxword = c_longlong


# Type of addresses. #
Elf32_Addr = c_uint
Elf64_Addr = c_ulonglong

# Type of file offsets. #
Elf32_Off = c_uint
Elf64_Off = c_ulonglong

# Type for section indices, which are 16-bit quantities. #
Elf32_Section = c_ushort
Elf64_Section = c_ushort

# Type for version symbol information. #
Elf32_Versym = Elf32_Half
Elf64_Versym = Elf64_Half

# The ELF file header.  This appears at the start of every ELF file.  #

# ELF e_ident 
EI_NIDENT = 16

Elf32_Ehdr_Size = 52 # ELF32 header size 
Elf64_Ehdr_Size = 64 # ELF64 header size 

# Fields in the e_ident array.  The EI_* macros are indices into the array.  
# The macros under each EI_* macro are the values the byte may have.  

# ELF MAGIC File identification 
ELFMAG0 = 0x7f # Magic number byte 0 
ELFMAG1 = 'E'  # Magic number byte 1
ELFMAG2 = 'L'  # Magic number byte 2
ELFMAG3 = 'F'  # Magic number byte 3 
ELFMAG  = [ELFMAG0, ord(ELFMAG1), ord(ELFMAG2), ord(ELFMAG3)] 

# ELF File class 
ELFCLASSNONE = 0    # Invalid class
ELFCLASS32   = 1    # 32-bit objects 
ELFCLASS64   = 2    # 64-bit objects
ELFCLASS = {ELFCLASSNONE:'Invalid class',ELFCLASS32:'ELF32',ELFCLASS64:'ELF64'}

# ELF DATA encoding 
ELFDATANONE = 0     # Invalid data encoding
ELFDATA2LSB = 1     # 2's complement, little endian
ELFDATA2MSB = 2     # 2's complement, big endian 
ELFDATA = {ELFDATANONE:'Invalid data encoding',ELFDATA2LSB:'''2's complement, little endian''',ELFDATA2MSB:'''2's complement, big endian'''}

# ELF File version Value must be EV_CURRENT
# Legal values for e_version (version)
EV_NONE    = 0       # Invalid ELF version 
EV_CURRENT = 1       # Current version
ELFVERSION = {EV_NONE:'0 (Invalid)',EV_CURRENT:'1 (Current)'}

# ELF OS ABI identification
ELFOSABI_NONE       = 0   # UNIX System V ABI (UNIX - System V)
ELFOSABI_SYSV       = 0   # Alias
ELFOSABI_HPUX       = 1   # HP-UX 
ELFOSABI_NETBSD     = 2   # NetBSD 
ELFOSABI_LINUX      = 3   # Linux  
ELFOSABI_SOLARIS    = 6   # Sun Solaris
ELFOSABI_AIX        = 7   # IBM AIX 
ELFOSABI_IRIX       = 8   # SGI Irix
ELFOSABI_FREEBSD    = 9   # FreeBSD
ELFOSABI_TRU64      = 10  # Compaq TRU64 UNIX
ELFOSABI_MODESTO    = 11  # Novell Modesto
ELFOSABI_OPENBSD    = 12  # OpenBSD
ELFOSABI_ARM        = 97  # ARM 
ELFOSABI_STANDALONE = 255 # Standalone (embedded) application 

ELFOSABI = {ELFOSABI_SYSV:'UNIX - System V',ELFOSABI_HPUX:'HP-UX',ELFOSABI_NETBSD:'NetBSD',ELFOSABI_LINUX:'Linux',
            ELFOSABI_SOLARIS:'Sun Solaris',ELFOSABI_AIX:'IBM AIX',ELFOSABI_IRIX:'SGI Irix',ELFOSABI_FREEBSD:'FreeBSD',
            ELFOSABI_TRU64:'Compaq TRU64 UNIX',ELFOSABI_MODESTO:'Novell Modesto',ELFOSABI_OPENBSD:'OpenBSD',
            ELFOSABI_ARM:'ARM',ELFOSABI_STANDALONE:'Standalone (embedded) application'
}

# Legal values for e_type (object file type)

ET_NONE   = 0      # No file type
ET_REL    = 1      # Relocatable file 
ET_EXEC   = 2      # Executable file
ET_DYN    = 3      # Shared object file
ET_CORE   = 4      # Core file
ET_NUM    = 5      # Number of defined types
ET_LOOS   = 0xfe00 # OS-specific range start 
ET_HIOS   = 0xfeff # OS-specific range end 
ET_LOPROC = 0xff00 # Processor-specific range start 
ET_HIPROC = 0xffff # Processor-specific range end 
ELFTYPE = {ET_NONE:'No file type',ET_REL:'REL (Relocatable file)',ET_EXEC:'EXEC (Executable file)',ET_DYN:'DYN (Shared object file)',ET_CORE:'CORE (Core file)'}

# Legal values for e_machine (architecture)

EM_NONE        = 0      # No machine 
EM_M32         = 1      # AT&T WE 32100 
EM_SPARC       = 2      # SUN SPARC 
EM_386         = 3      # Intel 80386 
EM_68K         = 4      # Motorola m68k family 
EM_88K         = 5      # Motorola m88k family 
EM_860         = 7      # Intel 80860 
EM_MIPS        = 8      # MIPS R3000 big-endian 
EM_S370        = 9      # IBM System/370 
EM_MIPS_RS3_LE = 10     # MIPS R3000 little-endian 

EM_PARISC      = 15      # HPPA 
EM_VPP500      = 17      # Fujitsu VPP500 
EM_SPARC32PLUS = 18      # Sun's "v8plus" 
EM_960         = 19      # Intel 80960 
EM_PPC         = 20      # PowerPC 
EM_PPC64       = 21      # PowerPC 64-bit 
EM_S390        = 22      # IBM S390 

EM_V800        = 36      # NEC V800 series 
EM_FR20        = 37      # Fujitsu FR20 
EM_RH32        = 38      # TRW RH-32 
EM_RCE         = 39      # Motorola RCE 
EM_ARM         = 40      # ARM 
EM_FAKE_ALPHA  = 41      # Digital Alpha 
EM_SH          = 42      # Hitachi SH 
EM_SPARCV9     = 43      # SPARC v9 64-bit 
EM_TRICORE     = 44      # Siemens Tricore 
EM_ARC         = 45      # Argonaut RISC Core 
EM_H8_300      = 46      # Hitachi H8/300 
EM_H8_300H     = 47      # Hitachi H8/300H 
EM_H8S         = 48      # Hitachi H8S 
EM_H8_500      = 49      # Hitachi H8/500 
EM_IA_64       = 50      # Intel Merced 
EM_MIPS_X      = 51      # Stanford MIPS-X 
EM_COLDFIRE    = 52      # Motorola Coldfire 
EM_68HC12      = 53      # Motorola M68HC12 
EM_MMA         = 54      # Fujitsu MMA Multimedia Accelerator
EM_PCP         = 55      # Siemens PCP 
EM_NCPU        = 56      # Sony nCPU embeeded RISC 
EM_NDR1        = 57      # Denso NDR1 microprocessor 
EM_STARCORE    = 58      # Motorola Start*Core processor 
EM_ME16        = 59      # Toyota ME16 processor 
EM_ST100       = 60      # STMicroelectronic ST100 processor 
EM_TINYJ       = 61      # Advanced Logic Corp. Tinyj emb.fam
EM_X86_64      = 62      # AMD x86-64 architecture / Advanced Micro Devices X86-64
EM_PDSP        = 63      # Sony DSP Processor 

EM_FX66        = 66      # Siemens FX66 microcontroller 
EM_ST9PLUS     = 67      # STMicroelectronics ST9+ 8/16 mc 
EM_ST7         = 68      # STmicroelectronics ST7 8 bit mc 
EM_68HC16      = 69      # Motorola MC68HC16 microcontroller 
EM_68HC11      = 70      # Motorola MC68HC11 microcontroller 
EM_68HC08      = 71      # Motorola MC68HC08 microcontroller 
EM_68HC05      = 72      # Motorola MC68HC05 microcontroller 
EM_SVX         = 73      # Silicon Graphics SVx 
EM_ST19        = 74      # STMicroelectronics ST19 8 bit mc 
EM_VAX         = 75      # Digital VAX 
EM_CRIS        = 76      # Axis Communications 32-bit embedded processor 
EM_JAVELIN     = 77      # Infineon Technologies 32-bit embedded processor 
EM_FIREPATH    = 78      # Element 14 64-bit DSP Processor 
EM_ZSP         = 79      # LSI Logic 16-bit DSP Processor 
EM_MMIX        = 80      # Donald Knuth's educational 64-bit processor 
EM_HUANY       = 81      # Harvard University machine-independent object files 
EM_PRISM       = 82      # SiTera Prism 
EM_AVR         = 83      # Atmel AVR 8-bit microcontroller 
EM_FR30        = 84      # Fujitsu FR30 
EM_D10V        = 85      # Mitsubishi D10V 
EM_D30V        = 86      # Mitsubishi D30V 
EM_V850        = 87      # NEC v850 
EM_M32R        = 88      # Mitsubishi M32R 
EM_MN10300     = 89      # Matsushita MN10300 
EM_MN10200     = 90      # Matsushita MN10200 
EM_PJ          = 91      # picoJava 
EM_OPENRISC    = 92      # OpenRISC 32-bit embedded processor 
EM_ARC_A5      = 93      # ARC Cores Tangent-A5 
EM_XTENSA      = 94      # Tensilica Xtensa Architecture 

ELFMACHINE = {EM_NONE:'NONE',EM_M32:'AT&T WE 32100',EM_SPARC:'SUN SPARC',EM_386:'Intel 80386',EM_68K:'Motorola m68k family',EM_88K:'Motorola m88k family',EM_860:'Intel 80860',
EM_MIPS:'MIPS R3000 big-endian',EM_S370:'IBM System/370',EM_MIPS_RS3_LE:'MIPS R3000 little-endian',EM_PARISC:'HPPA',EM_VPP500:'Fujitsu VPP500',EM_SPARC32PLUS:'''Sun's "v8plus"''',
EM_960:'Intel 80960',EM_PPC:'PowerPC',EM_PPC64:'PowerPC 64-bit',EM_S390:'IBM S390',EM_V800:'NEC V800 series',EM_FR20:'Fujitsu FR20',EM_RH32:'TRW RH-32',EM_RCE:'Motorola RCE',EM_ARM:'ARM',
EM_FAKE_ALPHA:'Digital Alpha',EM_SH:'Hitachi SH',EM_SPARCV9:'SPARC v9 64-bit',EM_TRICORE:'Siemens Tricore',EM_ARC:'Argonaut RISC Core',EM_H8_300:'Hitachi H8/300',
EM_H8_300H:'Hitachi H8/300H',EM_H8S:'Hitachi H8S',EM_H8_500:'Hitachi H8/500',EM_IA_64:'Intel Merced',EM_MIPS_X:'Stanford MIPS-X',EM_COLDFIRE:'Motorola Coldfire',
EM_68HC12:'Motorola M68HC12',EM_MMA:'Fujitsu MMA Multimedia Accelerator',EM_PCP:'Siemens PCP',EM_NCPU:'Sony nCPU embeeded RISC',EM_NDR1:'Denso NDR1 microprocessor',
EM_STARCORE:'Motorola Start*Core processor',EM_ME16:'Toyota ME16 processor',EM_ST100:'STMicroelectronic ST100 processor',EM_TINYJ:'Advanced Logic Corp. Tinyj emb.fam',
EM_X86_64:'Advanced Micro Devices X86-64',EM_PDSP:'Sony DSP Processor',EM_FX66:'Siemens FX66 microcontroller',EM_ST9PLUS:'STMicroelectronics ST9+ 8/16 mc',EM_ST7:'STmicroelectronics ST7 8 bit mc',
EM_68HC16:'Motorola MC68HC16 microcontroller',EM_68HC11:'Motorola MC68HC11 microcontroller',EM_68HC08:'Motorola MC68HC08 microcontroller',EM_68HC05:'Motorola MC68HC05 microcontroller',
EM_SVX:'Silicon Graphics SVx',EM_ST19:'STMicroelectronics ST19 8 bit mc',EM_VAX:'Digital VAX',EM_CRIS:'Axis Communications 32-bit embedded processor',EM_JAVELIN:'Infineon Technologies 32-bit embedded processor',
EM_FIREPATH:'Element 14 64-bit DSP Processor',EM_ZSP:'LSI Logic 16-bit DSP Processor',EM_MMIX:'''Donald Knuth's educational 64-bit processor''',EM_HUANY:'Harvard University machine-independent object files',
EM_PRISM:'SiTera Prism',EM_AVR:'Atmel AVR 8-bit microcontroller',EM_FR30:'Fujitsu FR30',EM_D10V:'Mitsubishi D10V',EM_D30V:'Mitsubishi D30V',EM_V850:'NEC v850',EM_M32R:'Mitsubishi M32R',
EM_MN10300:'Matsushita MN10300',EM_MN10200:'Matsushita MN10200',EM_PJ:'picoJava',EM_OPENRISC:'OpenRISC 32-bit embedded processor',EM_ARC_A5:'ARC Cores Tangent-A5',EM_XTENSA:'Tensilica Xtensa Architecture',
}

# Special section indices.  

SHN_UNDEF     = 0           # Undefined section 
SHN_LORESERVE = 0xff00      # Start of reserved indices 
SHN_LOPROC    = 0xff00      # Start of processor-specific 
SHN_BEFORE    = 0xff00      # Order section before all others (Solaris).  
SHN_AFTER     = 0xff01      # Order section after all others (Solaris).  
SHN_HIPROC    = 0xff1f      # End of processor-specific 
SHN_LOOS      = 0xff20      # Start of OS-specific 
SHN_HIOS      = 0xff3f      # End of OS-specific 
SHN_ABS       = 0xfff1      # Associated symbol is absolute 
SHN_COMMON    = 0xfff2      # Associated symbol is common 
SHN_XINDEX    = 0xffff      # Index is in extra table.  
SHN_HIRESERVE = 0xffff      # End of reserved indices 


# Legal values for sh_type (section type)

SHT_NULL          = 0          # Section header table entry unused 
SHT_PROGBITS      = 1          # Program data 
SHT_SYMTAB        = 2          # Symbol table 
SHT_STRTAB        = 3          # String table 
SHT_RELA          = 4          # Relocation entries with addends 
SHT_HASH          = 5          # Symbol hash table 
SHT_DYNAMIC       = 6          # Dynamic linking information 
SHT_NOTE          = 7          # Notes 
SHT_NOBITS        = 8          # Program space with no data (bss) 
SHT_REL           = 9          # Relocation entries, no addends 
SHT_SHLIB         = 10         # Reserved 
SHT_DYNSYM        = 11         # Dynamic linker symbol table 
SHT_INIT_ARRAY    = 14         # Array of constructors 
SHT_FINI_ARRAY    = 15         # Array of destructors 
SHT_PREINIT_ARRAY = 16         # Array of pre-constructors 
SHT_GROUP         = 17         # Section group 
SHT_SYMTAB_SHNDX  = 18         # Extended section indeces 
SHT_LOOS          = 0x60000000 # Start OS-specific.  
SHT_GNU_HASH      = 0x6ffffff6 # GNU-style hash table.  
SHT_GNU_LIBLIST   = 0x6ffffff7 # Prelink library list 
SHT_CHECKSUM      = 0x6ffffff8 # Checksum for DSO content.  
SHT_LOSUNW        = 0x6ffffffa # Sun-specific low bound.  
SHT_SUNW_move     = 0x6ffffffa
SHT_SUNW_COMDAT   = 0x6ffffffb
SHT_SUNW_syminfo  = 0x6ffffffc
SHT_GNU_verdef    = 0x6ffffffd # Version definition section.  
SHT_GNU_verneed   = 0x6ffffffe # Version needs section.  
SHT_GNU_versym    = 0x6fffffff # Version symbol table.  
SHT_HISUNW        = 0x6fffffff # Sun-specific high bound.  
SHT_HIOS          = 0x6fffffff # End OS-specific type 
SHT_LOPROC        = 0x70000000 # Start of processor-specific 
SHT_HIPROC        = 0x7fffffff # End of processor-specific 
SHT_LOUSER        = 0x80000000 # Start of application-specific 
SHT_HIUSER        = 0x8fffffff # End of application-spec

ELFSHTYPE = {SHT_NULL:'NULL',SHT_PROGBITS:'PROGBITS',SHT_SYMTAB:'SYMTAB',SHT_STRTAB:'STRTAB',SHT_RELA:'RELA',SHT_HASH:'HASH',SHT_DYNAMIC:'DYNAMIC',
SHT_NOTE:'NOTE',SHT_NOBITS:'NOBITS',SHT_REL:'REL',SHT_SHLIB:'SHLIB',SHT_DYNSYM:'DYNSYM',SHT_INIT_ARRAY:'INIT_ARRAY',
SHT_FINI_ARRAY:'FINI_ARRAY',SHT_PREINIT_ARRAY:'PREINIT_ARRAY',SHT_GROUP:'GROUP',SHT_SYMTAB_SHNDX:'SYMTAB_SHNDX',
SHT_GNU_HASH:'GNU_HASH',SHT_GNU_LIBLIST:'GNU_LIBLIST',SHT_CHECKSUM:'CHECKSUM',SHT_GNU_verdef:'GNU_verdef',SHT_GNU_verneed:"VERNEED",SHT_GNU_versym:"VERSYM"
}

# Legal values for sh_flags (section flags).  

SHF_WRITE             = (1 << 0)   # Writable 
SHF_ALLOC             = (1 << 1)   # Occupies memory during execution 
SHF_EXECINSTR         = (1 << 2)   # Executable
SHF_MERGE             = (1 << 4)   # Might be merged
SHF_STRINGS           = (1 << 5)   # Contains nul-terminated strings
SHF_INFO_LINK         = (1 << 6)   # `sh_info' contains SHT index
SHF_LINK_ORDER        = (1 << 7)   # Preserve order after combining
SHF_OS_NONCONFORMING  = (1 << 8)   # Non-standard OS specific handling required */
SHF_GROUP             = (1 << 9)   # Section is member of a group. 
SHF_TLS               = (1 << 10)  # Section hold thread-local data. 
SHF_MASKOS            = 0x0ff00000 # OS-specific. 
SHF_MASKPROC          = 0xf0000000 # Processor-specific
SHF_ORDERED           = (1 << 30)  # Special ordering requirement (Solaris).  */
SHF_EXCLUDE           = (1 << 31)  # Section is excluded unless referenced or allocated (Solaris).*/

ELFSHFLAG = {SHF_WRITE:'W',SHF_ALLOC:'A',SHF_EXECINSTR:'X',SHF_MERGE:'M',SHF_STRINGS:'S',SHF_INFO_LINK:'I',SHF_LINK_ORDER:'L',SHF_GROUP:'G',SHF_TLS:'T',SHF_MASKOS:'o',SHF_MASKPROC:'p',SHF_EXCLUDE:'E'}

# Section group handling.  
GRP_COMDAT = 0x1     # Mark group as COMDAT.


# Legal values for p_type (segment type)

PT_NULL    = 0   # Program header table entry unused 
PT_LOAD    = 1   # Loadable program segment 
PT_DYNAMIC = 2   # Dynamic linking information 
PT_INTERP  = 3   # Program interpreter 
PT_NOTE    = 4   # Auxiliary information 
PT_SHLIB   = 5   # Reserved 
PT_PHDR    = 6   # Entry for header table itself 
PT_TLS     = 7   # Thread-local storage segment
PT_LOOS         = 0x60000000  # Start of OS-specific 
PT_GNU_EH_FRAME = 0x6474e550  # GCC .eh_frame_hdr segment 
PT_GNU_STACK    = 0x6474e551  # Indicates stack executability 
PT_GNU_RELRO    = 0x6474e552  # Read-only after relocation 
PT_LOSUNW       = 0x6ffffffa  #
PT_SUNWBSS      = 0x6ffffffa  # Sun Specific segment 
PT_SUNWSTACK    = 0x6ffffffb  # Stack segment 
PT_HISUNW       = 0x6fffffff  #
PT_HIOS         = 0x6fffffff  # End of OS-specific 
PT_LOPROC       = 0x70000000  # Start of processor-specific 
PT_HIPROC       = 0x7fffffff  # End of processor-specific 

ELFPHTYPE = {PT_NULL:'NULL',PT_LOAD:'LOAD',PT_DYNAMIC:'DYNAMIC',PT_INTERP:'INTERP',PT_NOTE:'NOTE',PT_SHLIB:'SHLIB',PT_PHDR:'PHDR',PT_TLS:'TLS',
PT_LOOS:'LOOS',PT_GNU_EH_FRAME:'GNU_EH_FRAME',PT_GNU_STACK:'GNU_STACK',PT_GNU_RELRO:'GNU_RELRO',PT_LOSUNW:'LOSUNW',PT_SUNWBSS:'SUNWBSS',
PT_SUNWSTACK:'SUNWSTACK',PT_HISUNW:'HISUNW',PT_HIOS:'HIOS',PT_LOPROC:'LOPROC',PT_HIPROC:'HIPROC',}

# Legal values for p_flags (segment flags)

PF_X         = (1 << 0)  # Segment is executable 
PF_W         = (1 << 1)  # Segment is writable 
PF_R         = (1 << 2)  # Segment is readable 
PF_MASKOS    = 0x0ff00000  # OS-specific 
PF_MASKPROC  = 0xf0000000  # Processor-specific

ELFPHFLAG = {PF_X:'E',PF_W:'W',PF_R:'R'}

# E_IDENT
class E_IDENT(Structure):

    _fields_ = [
                ('e_mag0',c_ubyte),       # File identification / Magic number byte 0
                ('e_mag1',c_ubyte),       # File identification / Magic number byte 1
                ('e_mag2',c_ubyte),       # File identification / Magic number byte 2
                ('e_mag3',c_ubyte),       # File identification / Magic number byte 3
                ('e_class',c_ubyte),      # File class byte
                ('e_data',c_ubyte),       # Data encoding byte
                ('e_version',c_ubyte),    # File version byte
                ('e_osabi',c_ubyte),      # OS ABI identification
                ('e_abiversion',c_ubyte), # ABI version
                ('e_pad', c_ubyte * 7),   # padding bytes
    ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass

    def iself(self):
        return True if self.e_mag0 == ELFMAG0 and self.e_mag1 == ord(ELFMAG1) and self.e_mag2 == ord(ELFMAG2) and self.e_mag3 == ord(ELFMAG3) else False

    def is32bit(self):
        return True if self.e_class == ELFCLASS32 else False

    def is64bit(self):
        return True if self.e_class == ELFCLASS64 else False


# The ELF file header.  This appears at the start of every ELF file.

class Elf32_Ehdr(Structure):

    _fields_ = [
            ('e_ident',E_IDENT),        # Magic number and other info 
            ('e_type',Elf32_Half),      # Object file type 
            ('e_machine',Elf32_Half),   # Architecture
            ('e_version',Elf32_Word),   # Object file version
            ('e_entry',Elf32_Addr),     # Entry point virtual address
            ('e_phoff',Elf32_Off),      # Program header table file offset 
            ('e_shoff',Elf32_Off),      # Section header table file offset 
            ('e_flags',Elf32_Word),     # Processor-specific flags 
            ('e_ehsize',Elf32_Half),    # ELF header size in bytes 
            ('e_phentsize',Elf32_Half), # Program header table entry size 
            ('e_phnum',Elf32_Half),     # Program header table entry count 
            ('e_shentsize',Elf32_Half), # Section header table entry size 
            ('e_shnum',Elf32_Half),     # Section header table entry count 
            ('e_shstrndx',Elf32_Half),  # Section header string table index 
    ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass

class Elf64_Ehdr(Structure):

    _fields_ = [
            ('e_ident',E_IDENT),        # Magic number and other info 
            ('e_type',Elf64_Half),      # Object file type 
            ('e_machine',Elf64_Half),   # Architecture 
            ('e_version',Elf64_Word),   # Object file version 
            ('e_entry',Elf64_Addr),     # Entry point virtual address 
            ('e_phoff',Elf64_Off),      # Program header table file offset 
            ('e_shoff',Elf64_Off),      # Section header table file offset 
            ('e_flags',Elf64_Word),     # Processor-specific flags 
            ('e_ehsize',Elf64_Half),    # ELF header size in bytes 
            ('e_phentsize',Elf64_Half), # Program header table entry size 
            ('e_phnum',Elf64_Half),     # Program header table entry count 
            ('e_shentsize',Elf64_Half), # Section header table entry size 
            ('e_shnum',Elf64_Half),     # Section header table entry count 
            ('e_shstrndx',Elf64_Half),  # Section header string table index 
    ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass

# Section header
class Elf32_Shdr(Structure):

    _fields_ = [
              ('sh_name',Elf32_Word),      # Section name (string tbl index)
              ('sh_type',Elf32_Word),      # Section type
              ('sh_flags',Elf32_Word),     # Section flags
              ('sh_addr',Elf32_Addr),      # Section virtual addr at execution
              ('sh_offset',Elf32_Off),     # Section file offset
              ('sh_size',Elf32_Word),      # Section size in bytes
              ('sh_link',Elf32_Word),      # Link to another section
              ('sh_info',Elf32_Word),      # Additional section information
              ('sh_addralign',Elf32_Word), # Section alignment
              ('sh_entsize',Elf32_Word),   # Entry size if section holds table 
  ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass


class Elf64_Shdr(Structure):

    _fields_ = [
              ('sh_name',Elf64_Word),       # Section name (string tbl index)
              ('sh_type',Elf64_Word),       # Section type
              ('sh_flags',Elf64_Xword),     # Section flags
              ('sh_addr',Elf64_Addr),       # Section virtual addr at execution
              ('sh_offset',Elf64_Off),      # Section file offset
              ('sh_size',Elf64_Xword),      # Section size in bytes
              ('sh_link',Elf64_Word),       # Link to another section
              ('sh_info',Elf64_Word),       # Additional section information
              ('sh_addralign',Elf64_Xword), # Section alignment
              ('sh_entsize',Elf64_Xword),   # Entry size if section holds table 
  ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass

# Program segment header
class Elf32_Phdr(Structure):

    _fields_ = [
              ('p_type',Elf32_Word),   # Segment type 
              ('p_offset',Elf32_Off),  # Segment file offset 
              ('p_vaddr',Elf32_Addr),  # Segment virtual address
              ('p_paddr',Elf32_Addr),  # Segment physical address
              ('p_filesz',Elf32_Word), # Segment size in file 
              ('p_memsz',Elf32_Word),  # Segment size in memory 
              ('p_flags',Elf32_Word),  # Segment flags
              ('p_align',Elf32_Word),  # Segment alignment
    ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass

class Elf64_Phdr(Structure):

    _fields_ = [
              ('p_type',Elf64_Word),   # Segment type 
              ('p_flags',Elf64_Word),  # Segment flags
              ('p_offset',Elf64_Off),  # Segment file offset 
              ('p_vaddr',Elf64_Addr),  # Segment virtual address
              ('p_paddr',Elf64_Addr),  # Segment physical address
              ('p_filesz',Elf64_Xword), # Segment size in file 
              ('p_memsz',Elf64_Xword),  # Segment size in memory 
              ('p_align',Elf64_Xword),  # Segment alignment
    ]

    def __new__(self, buffer):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass



e_ident_show  = '''Magic: {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:s} 
Class: {:s} 
Data: {:s} 
Version: {:s}
OS/ABI: {:s}
ABI Version: {:d}'''

Elf32_Ehdr_show = '''Type: {:s}
Machine: {:s}
Version: {:#x}
Entry point address: {:#x}
Start of program headers: {:d} (bytes into file)
Start of section headers: {:d} (bytes into file)
Flags: {:#x}
Size of this header: {:d} (bytes)
Size of program headers: {:d} (bytes)
Number of program headers: {:d}
Size of section headers: {:d} (bytes)
Number of section headers: {:d}
Section header string table index: {:d}
'''

Section_FLag_info ='''Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)
'''

class ELF32(object):

    def __init__(self,data):
        self.data = data
        self.Parse()

    def Parse(self):
        # ELF header
        self.data.seek(0,0)
        self.header = Elf32_Ehdr(self.data.read(Elf32_Ehdr_Size))

        # ELF section header   
        self.data.seek(self.header.e_shoff,0)
        
        section_headers_data = self.data.read(self.header.e_shentsize * self.header.e_shnum)
        # Get Section Headers
        self.section_headers = [Elf32_Shdr(section_headers_data[i * self.header.e_shentsize:(i + 1) * self.header.e_shentsize]) for i in range(0,self.header.e_shnum)]
        #self.section_headers = []
        #for i in range(0,self.header.e_shnum):
        #    print(len(section_headers_data[i * self.header.e_shentsize:(i + 1)*self.header.e_shentsize]))
        #    self.section_headers.append(Elf32_Shdr(section_headers_data[i * self.header.e_shentsize:(i + 1)*self.header.e_shentsize]))

        # Get Section Names
        self.section_names = []
        for i in range(0,self.header.e_shnum):
            offset = self.section_headers[self.header.e_shstrndx].sh_offset + self.section_headers[i].sh_name
            self.section_names.append(self.ReadStr(offset))

        # Program segment header
        self.data.seek(self.header.e_phoff,0)
        segment_headers_data = self.data.read(self.header.e_phentsize * self.header.e_phnum)
        self.segment_headers = [Elf32_Phdr(segment_headers_data[i * self.header.e_phentsize:(i + 1) * self.header.e_phentsize]) for i in range(0,self.header.e_phnum)]
    
    def ReadStr(self,offset,end='\0',len=32):
        self.data.seek(offset,0)
        chars = ""
        for char in self.data.read(len).decode():
            if not char == end:
                chars = chars + char
            else:
                break
        return chars

    def Output(self):
        return self.header,self.section_names,self.section_headers,self.segment_headers

class ELF64(object):

    def __init__(self,data):
        self.data = data
        self.Parse()

    def Parse(self):
        # ELF header
        self.data.seek(0,0)
        self.header = Elf64_Ehdr(self.data.read(Elf64_Ehdr_Size))

        # ELF section header   
        self.data.seek(self.header.e_shoff,0)
        section_headers_data = self.data.read(self.header.e_shentsize * self.header.e_shnum)
        # Get Section Headers
        self.section_headers = [Elf64_Shdr(section_headers_data[i * self.header.e_shentsize:(i + 1) * self.header.e_shentsize]) for i in range(0,self.header.e_shnum)]

        # Get Section Names
        self.section_names = []
        for i in range(0,self.header.e_shnum):
            offset = self.section_headers[self.header.e_shstrndx].sh_offset + self.section_headers[i].sh_name
            self.section_names.append(self.ReadStr(offset))

        # Program segment header
        self.data.seek(self.header.e_phoff,0)
        segment_headers_data = self.data.read(self.header.e_phentsize * self.header.e_phnum)
        self.segment_headers = [Elf64_Phdr(segment_headers_data[i * self.header.e_phentsize:(i + 1) * self.header.e_phentsize]) for i in range(0,self.header.e_phnum)]
    
    def ReadStr(self,offset,end='\0',len=32):
        self.data.seek(offset,0)
        chars = ""
        for char in self.data.read(len).decode():
            if not char == end:
                chars = chars + char
            else:
                break
        return chars

    def Output(self):
        return self.header,self.section_names,self.section_headers,self.segment_headers

class ELF(object):

    def __init__(self,filepath):
        with open(filepath, 'rb') as fr:
            #self.data = io.StringIO(fr.read().decode())
            self.data = io.BytesIO(fr.read())

        self.data.seek(0,0)
        self.e_ident = E_IDENT(self.data.read(EI_NIDENT))

        if self.e_ident.iself() and self.e_ident.is32bit():
            self.elffile = ELF32(self.data)
            self.header,self.section_names,self.section_headers,self.segment_headers = self.elffile.Output()
        elif self.e_ident.iself() and self.e_ident.is64bit():
            self.elffile = ELF64(self.data)
            self.header,self.section_names,self.section_headers,self.segment_headers = self.elffile.Output()
        else:
            pass

        self.section2segment()

    def readstr(self,offset,end='\0',len=32):
        self.data.seek(offset,0)
        chars = ""
        for char in self.data.read(len).decode():
            if not char == end:
                chars = chars + char
            else:
                break
        return chars

    def section2segment(self):
        self.section2segment_result = []
        for i in range(0,self.header.e_phnum):
            phdr = self.segment_headers[i]
            if phdr.p_memsz == 0:
                self.section2segment_result.append([])
                continue
            else: 
                sections = []
                for index,section in enumerate(self.section_headers):
                    # section must have Flag ALLOC
                    if not section.sh_flags & SHF_ALLOC:
                        continue

                    if not bool(phdr.p_type == PT_TLS) == bool(section.sh_flags & SHF_TLS):
                        continue

                    if (section.sh_addr >= phdr.p_vaddr) and (section.sh_addr + section.sh_size) <= (phdr.p_vaddr + phdr.p_memsz):
                        sections.append(self.section_names[index])
                    else:
                        pass
            self.section2segment_result.append(sections)

    def elfphdrtype(self,p_type):

      if p_type > PT_LOOS and p_type< PT_HIOS:
          return "LOOS+%x" % (p_type - PT_LOOS)
      elif p_type > PT_LOPROC and p_type< PT_HIPROC:
          return "LOPROC+%x" % (p_type - PT_LOPROC)
      else:
          return "%#x" % p_type

    def PrintELFHeader(self):
        header = self.header
        # e_ident
        print(e_ident_show.format(header.e_ident.e_mag0,header.e_ident.e_mag1,header.e_ident.e_mag2,header.e_ident.e_mag3,header.e_ident.e_class,
            header.e_ident.e_data,header.e_ident.e_version,header.e_ident.e_osabi,header.e_ident.e_abiversion," ".join(['%02x' % pad for pad in header.e_ident.e_pad]),
            ELFCLASS[header.e_ident.e_class],ELFDATA[header.e_ident.e_data],ELFVERSION[header.e_ident.e_version],ELFOSABI[header.e_ident.e_osabi],header.e_ident.e_abiversion))
    
        # header
        print (Elf32_Ehdr_show.format(ELFTYPE[header.e_type],ELFMACHINE[header.e_machine],header.e_version,header.e_entry,header.e_phoff,header.e_shoff,header.e_flags,
            header.e_ehsize,header.e_phentsize,header.e_phnum,header.e_shentsize,header.e_shnum,header.e_shstrndx))

    def OutputELFHeader(self):
        header = self.header
        magic_info = [header.e_ident.e_mag0,
                 header.e_ident.e_mag1, header.e_ident.e_mag2, header.e_ident.e_mag3, header.e_ident.e_class,
                 header.e_ident.e_data, header.e_ident.e_version, header.e_ident.e_osabi, header.e_ident.e_abiversion]
        magic_info.extend(header.e_ident.e_pad)

        return {'Magic':magic_info,#list
                  'Class':ELFCLASS[header.e_ident.e_class],#string
                  'Data':ELFDATA[header.e_ident.e_data],#string
                  'Version':ELFVERSION[header.e_ident.e_version],#string
                  'OS/ABI':ELFOSABI[header.e_ident.e_osabi],#string
                  'ABI Version':header.e_ident.e_abiversion,#oct int
                  'Type':ELFTYPE[header.e_type],#string
                  'Machine':ELFMACHINE[header.e_machine],#string
                  'Version':'{:#x}'.format(header.e_version),# hex int
                  'Entry point address':'{:#x}'.format(header.e_entry),# hex int
                  'Start of program headers':header.e_phoff,# oct int
                  'Start of section headers':header.e_shoff,# oct int
                'Flags':'{:#x}'.format(header.e_flags),# hex int
                'Size of this header': header.e_ehsize,# oct int
                'Size of program headers': header.e_phentsize,#oct int
                'Number of program headers':header.e_phnum,#oct int
                'Size of section headers': header.e_shentsize,#oct int
                'Number of section headers':header.e_shnum,#oct int
                'Section header string table index':header.e_shstrndx,#oct int
        }



    def PrintELFShdr(self):
        ELF32title = '[{:>2s}] {:<20s} {:<16s} {:<8s} {:<6s} {:<6s} {:>2s} {:>3s} {:>2s} {:>3s} {:>2s}'
        ELF32content = '[{:2d}] {:<20s} {:<16s} {:0>8x} {:0>6x} {:0>6x} {:0>2x} {:>3s} {:>2d} {:>3d} {:>2d}'
        ELF64title = '[{:>2s}] {:<16s} {:<16s} {:>16s} {:<8s}\n     {:<16s} {:<16s} {:>6s} {:>4s} {:>4s} {:>6s}'
        ELF64content = '[{:2d}] {:<16s} {:<16s} {:0>16x} {:0>8x}\n     {:0>16x} {:0>16x} {:>6s} {:>4d} {:>4d} {:>6d}'        
        #print('There are {:d} section headers, starting at offset {:#x}:\n\nSection Headers:').format(self.header.e_shnum,self.header.e_shoff)
        if self.e_ident.is32bit():
            title, content= ELF32title,ELF32content   
        elif self.e_ident.is64bit():
            title, content= ELF64title,ELF64content
        else:
            return

        print(title.format('Nr','Name','Type','Addr','Off','Size','ES','Flg','Lk','Inf','Al'))
        for i in range(0,self.header.e_shnum):
            shdr = self.section_headers[i]
            sh_name = self.section_names[i]
            sh_flags = ''.join([mark for flag,mark in ELFSHFLAG.items() if shdr.sh_flags & flag])
            print(content.format(i,sh_name,ELFSHTYPE.get(shdr.sh_type,"%#x" % shdr.sh_type),shdr.sh_addr,shdr.sh_offset,shdr.sh_size,shdr.sh_entsize,sh_flags,shdr.sh_link,shdr.sh_info,shdr.sh_addralign))

    def OutputELFShdr(self):
        output = []

        if self.e_ident.is32bit():
            for i,shdr in enumerate(self.section_headers):
                #shdr = self.section_headers[i]
                sh_name = self.section_names[i]
                sh_flags = ''.join([mark for flag, mark in ELFSHFLAG.items() if shdr.sh_flags & flag])
                output.append(
                    {'Name': sh_name,
                     'Type': ELFSHTYPE.get(shdr.sh_type, "%#x" % shdr.sh_type),
                     'Addr': '{:0>8x}'.format(shdr.sh_addr), # hex int
                     'Off': '{:0>6x}'.format(shdr.sh_offset), # hex int
                     'Size': '{:0>6x}'.format(shdr.sh_size), # hex int
                     'ES': '{:0>2x}'.format(shdr.sh_entsize), # hex int
                     'Flg': sh_flags,# string
                     'Lk': shdr.sh_link, # oct int
                     'Inf': shdr.sh_info, # oct int
                     'Al': shdr.sh_addralign}) #oct int
        elif self.e_ident.is64bit():
            for i,shdr in enumerate(self.section_headers):
                #shdr = self.section_headers[i]
                sh_name = self.section_names[i]
                sh_flags = ''.join([mark for flag, mark in ELFSHFLAG.items() if shdr.sh_flags & flag])
                output.append(
                    {'Name': sh_name,
                     'Type': ELFSHTYPE.get(shdr.sh_type, "%#x" % shdr.sh_type),
                     'Addr': '{:0>16x}'.format(shdr.sh_addr), # hex int
                     'Off': '{:0>8x}'.format(shdr.sh_offset), # hex int
                     'Size': '{:0>16x}'.format(shdr.sh_size), # hex int
                     'ES': '{:0>16x}'.format(shdr.sh_entsize), # hex int
                     'Flg': sh_flags, # string
                     'Lk': shdr.sh_link, # oct int
                     'Inf': shdr.sh_info, # oct int
                     'Al': shdr.sh_addralign}) #oct int
        else:
            return
        return output

    def PrintELFPhdr(self):
        #print('Elf file type is {:s}').format(ELFTYPE[self.header.e_type],)
        #print('Entry point {:#x}').format(self.header.e_entry,)
        #print('There are {:d} program headers, starting at offset {:d}\n\nProgram Headers:').format(self.header.e_phnum,self.header.e_phoff)
        ELF32title = '{:<14s} {:<8s} {:<10s} {:<10s} {:<7s} {:<7s} {:<3s} {:<6s}'
        ELF32content = '{:<14s} 0x{:0>6x} 0x{:0>8x} 0x{:0>8x} 0x{:0>5x} 0x{:0>5x} {:<3s} 0x{:<4x}'
        ELF64title = '{:<14s} {:<18s} {:<18s} {:<18s} \n               {:<18s} {:<18s} {:<6s} {:<6s}'
        ELF64content = '{:<14s} 0x{:0>16x} 0x{:0>16x} 0x{:0>16x} \n               0x{:0>16x} 0x{:0>16x} {:<6s} {:<6x}'

        if self.e_ident.is32bit():
            title,content = ELF32title, ELF32content
        elif self.e_ident.is64bit():
            title, content= ELF64title,ELF64content
        else:
            return

        print(title.format('Type','Offset','VirtAddr','PhysAddr','FileSiz','MemSiz','Flg','Align'))
        for i in range(0,self.header.e_phnum):
            phdr = self.segment_headers[i]
            ph_flags = ''.join([mark for flag,mark in ELFPHFLAG.items() if phdr.p_flags & flag])
            print(content.format(ELFPHTYPE.get(phdr.p_type,self.elfphdrtype(phdr.p_type)),phdr.p_offset,phdr.p_vaddr,phdr.p_paddr,phdr.p_filesz,phdr.p_memsz,ph_flags,phdr.p_align))
            
            if phdr.p_type == PT_INTERP:
                print ("\t[Requesting program interpreter: %s]" % self.readstr(offset = phdr.p_offset))

        print('\nSection to Segment mapping:\nSegment Sections...')
        for index,sections in enumerate(self.section2segment_result):
            print('{:0>2d}    {:s}'.format(index," ".join(sections)))

    def OutputELFPhdr(self):
        output = []

        if self.e_ident.is32bit():
            for i,phdr in enumerate(self.segment_headers):
                ph_flags = ''.join([mark for flag, mark in ELFPHFLAG.items() if phdr.p_flags & flag])

                output.append(
                    {'Type':ELFPHTYPE.get(phdr.p_type, self.elfphdrtype(phdr.p_type)), #string
                     'Offset':'0x{:0>6x}'.format(phdr.p_offset), #hex
                     'VirtAddr':'0x{:0>8x}'.format(phdr.p_vaddr),#hex
                     'PhysAddr':'0x{:0>8x}'.format(phdr.p_paddr),#hex
                     'FileSiz':'0x{:0>5x}'.format(phdr.p_filesz),#hex
                     'MemSiz':'0x{:0>5x}'.format(phdr.p_memsz),#hex
                     'Flg':ph_flags, #string
                     'Align':'0x{:<4x}'.format(phdr.p_align)})#hex
        elif self.e_ident.is64bit():
            for i,phdr in enumerate(self.segment_headers):
                ph_flags = ''.join([mark for flag, mark in iter(ELFPHFLAG.items()) if phdr.p_flags & flag])
                output.append(
                    {'Type':ELFPHTYPE.get(phdr.p_type, self.elfphdrtype(phdr.p_type)),
                     'Offset':'0x{:0>16x}'.format(phdr.p_offset),
                     'VirtAddr':'0x{:0>16x}'.format(phdr.p_vaddr),
                     'PhysAddr':'0x{:0>16x}'.format(phdr.p_paddr),
                     'FileSiz':'0x{:0>16x}'.format(phdr.p_filesz),
                     'MemSiz':'0x{:0>16x}'.format(phdr.p_memsz),
                     'Flg':ph_flags,
                     'Align':'0x{:<6x}'.format(phdr.p_align)})
        else:
            return
        return output
        


    def Print(self):
        self.PrintELFHeader()
        self.PrintELFShdr()
        print(Section_FLag_info)
        self.PrintELFPhdr()



