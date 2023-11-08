# Palkeoramix decompiler. 

def storage:
  owner is addr at storage 0
  stor0 is uint256 at storage 0
  curatorAddress is addr at storage 1
  stor1 is uint256 at storage 1
  daoAddress is addr at storage 2
  stor2 is uint256 at storage 2
  counter is uint256 at storage 3
  unknown371fa854 is uint256 at storage 4
  unknown26f5a8c9 is uint256 at storage 5
  nextAddress is addr at storage 6
  stor6 is uint256 at storage 6
  unknown5970c915Address is addr at storage 7
  stor7 is uint256 at storage 7

def unknown26f5a8c9() payable: 
  return unknown26f5a8c9

def unknown371fa854() payable: 
  return unknown371fa854

def dao() payable: 
  return addr(daoAddress)

def next() payable: 
  return addr(nextAddress)

def unknown5970c915() payable: 
  return addr(unknown5970c915Address)

def counter() payable: 
  return counter

def owner() payable: 
  return addr(owner)

def curator() payable: 
  return addr(curatorAddress)

#
#  Regular functions
#

def unknown7f9f519f(uint256 _param1) payable: 
  require caller == addr(owner)
  unknown26f5a8c9 = _param1
  log 0xbab6859b: _param1
  return 1

def setDao(address _dao) payable: 
  require caller == addr(owner)
  uint256(stor2) = _dao or Mask(96, 160, uint256(stor2))
  log 0xce6a5015: _dao
  return 1

def setOwner(address _new) payable: 
  require caller == addr(owner)
  log NewOwner(address owner=_new)
  uint256(stor0) = _new or Mask(96, 160, uint256(stor0))
  return 1

def vote(uint256 _proposalID, bool _supportsProposal) payable: 
  require caller == addr(owner)
  call addr(daoAddress).vote(uint256 proposalID, bool supportsProposal) with:
       gas gas_remaining - 25050 wei
      args _proposalID, _supportsProposal
  require ext_call.success
  log 0x8bfa1f40: _proposalID, _supportsProposal
  return 1

def transfer(address _to, uint256 _value) payable: 
  require caller == addr(owner)
  call addr(daoAddress).transfer(address to, uint256 tokens) with:
       gas gas_remaining - 25050 wei
      args addr(_to), _value
  require ext_call.success
  log Transfer(
        address receiver=addr(_to),
        uint256 weiAmount=_value)
  return 1

def unknown625e847d() payable: 
  require caller == addr(owner)
  counter = 1
  call addr(unknown5970c915Address) with:
     value eth.balance(this.address) wei
       gas 0 wei
  call addr(daoAddress).splitDAO(uint256 proposalID, address newCurator) with:
       gas gas_remaining - 25050 wei
      args unknown371fa854, addr(curatorAddress)
  require ext_call.success
  return 1

def unknownc4463c80(uint256 _param1, uint256 _param2, uint256 _param3, uint256 _param4, uint256 _param5) payable: 
  require caller == addr(owner)
  uint256(stor6) = _param3 or Mask(96, 160, uint256(stor6))
  counter = 1
  uint256(stor1) = _param2 or Mask(96, 160, uint256(stor1))
  unknown371fa854 = _param1
  unknown26f5a8c9 = _param4
  uint256(stor7) = _param5 or Mask(96, 160, uint256(stor7))
  call addr(_param5) with:
     value eth.balance(this.address) wei
       gas 0 wei
  call addr(daoAddress).splitDAO(uint256 proposalID, address newCurator) with:
       gas gas_remaining - 25050 wei
      args unknown371fa854, addr(curatorAddress)
  require ext_call.success
  log 0xa1ab7317: unknown371fa854, addr(nextAddress)
  return 1

def _fallback() payable: # default function
  call addr(daoAddress).rewardAccount() with:
       gas gas_remaining - 25050 wei
  require ext_call.success
  if ext_call.return_data[12 len 20] != caller:
      log 0xa6af7265: ext_call.return_data
  else:
      if counter <= unknown26f5a8c9 - 1:
          counter++
          call addr(daoAddress).splitDAO(uint256 proposalID, address newCurator) with:
               gas gas_remaining - 25050 wei
              args unknown371fa854, addr(curatorAddress)
          require ext_call.success
      else:
          call addr(daoAddress).balanceOf(address tokenOwner) with:
               gas gas_remaining - 25050 wei
              args this.address
          require ext_call.success
          call addr(daoAddress).transfer(address to, uint256 tokens) with:
               gas gas_remaining - 25050 wei
              args addr(nextAddress), ext_call.return_data[0]
          counter = 1
  return 1


