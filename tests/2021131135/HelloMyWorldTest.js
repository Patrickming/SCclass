const { expect } = require("chai");

describe("HelloMyWorld contract", function () {

  let HelloMyWorld;
  let hardhatHelloMyWorld;
  let hardhatHelloMyWorldAddress;
  let hardhatHelloMyWorldBalance;
  let owner;
  let addr1;
  let addr2;
  let addrs;

  // `beforeEach` will run before each test, re-deploying the contract every
  // time. It receives a callback, which can be async.
  beforeEach(async function () {
    const libFactory = await ethers.getContractFactory("StringUtil");
    const libObj = await libFactory.deploy()
    await libObj.deployed()
    // Get the ContractFactory and Signers here.
    HelloMyWorld = await ethers.getContractFactory("HelloMyWorld",{
        libraries: {
            StringUtil: libObj.address
        }
    });
    [owner, addr1, addr2, ...addrs] = await ethers.getSigners();

    // To deploy our contract, we just have to call HelloMyWorld.deploy() and await
    // for it to be deployed(), which happens onces its transaction has been
    // mined.
    hardhatHelloMyWorld = await HelloMyWorld.deploy();
    await hardhatHelloMyWorld.deployed();

    hardhatHelloMyWorldAddress = hardhatHelloMyWorld.address;
    hardhatHelloMyWorldBalance = await ethers.provider.getBalance(hardhatHelloMyWorldAddress);
    hardhatHelloMyWorldBalance = 0;

    //var balancePromise = ethers.provider.getBalance(hardhatHelloMyWorldAddress);
    //balancePromise.then(function (result) {
    //  hardhatHelloMyWorldBalance = result;
    //  //console.log("beforeEach hardhatHelloMyWorldBalance:", hardhatHelloMyWorldBalance);
    //});
  });

  // You can nest describe calls to create subsections.
  describe("Deployment", function () {
    // `it` is another Mocha function. This is the one you use to define your
    // tests. It receives the test name, and a callback function.
    
    it("Should be 0 balance", async function () {
      // Why compare balance with string "0"?
      expect(hardhatHelloMyWorldBalance.toString()).to.equal("0");
    });
  });

  describe("Transactions", function () {
  	  var expectedString = "Hello World! My name is Xia Ruoming. My class number is 214."
    it("Should be '" + expectedString + "'", async function () {
    	 var result = await hardhatHelloMyWorld.myFirstHelloWorld();
      expect(result).to.equal(expectedString);
    });
  });
});