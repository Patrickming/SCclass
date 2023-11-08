// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

contract PolymorphismDemoA {
    function vfunc(uint inputOne, uint inputTwo) virtual public pure returns (uint output) {
        return inputOne + inputTwo;
    }
}

contract PolymorphismDemoB is PolymorphismDemoA{
    function vfunc(uint inputOne, uint inputTwo) override public pure returns (uint output) {
        return inputOne - inputTwo;
    }
}

contract PolymorphismDemoC is PolymorphismDemoA {
    function vfunc(uint inputOne, uint inputTwo) override public pure returns (uint output) {
        return inputOne * inputTwo;
    }
}

contract PolymorphismDemoD is PolymorphismDemoA {
    function vfunc(uint inputOne, uint inputTwo) override public pure returns (uint output) {
        return inputOne / inputTwo;
    }
}

contract PolymorphismDemo {
    enum AlgorithmSelector{Add, Reduce, Multiply, Divide}
    PolymorphismDemoA polymorphismDemoA = new PolymorphismDemoA();
    PolymorphismDemoB polymorphismDemoB = new PolymorphismDemoB();
    PolymorphismDemoC polymorphismDemoC = new PolymorphismDemoC();
    PolymorphismDemoD polymorphismDemoD = new PolymorphismDemoD();

    function polymorphismDemo(AlgorithmSelector algorithmSelector, uint inputOne, uint inputTwo) 
    public view 
    returns (uint output) {
        if (algorithmSelector == AlgorithmSelector.Add) {
            output = polymorphismCall(polymorphismDemoA, inputOne, inputTwo);
        }
        else if (algorithmSelector == AlgorithmSelector.Reduce) {
            output = polymorphismCall(polymorphismDemoB, inputOne, inputTwo);
        }
        else if (algorithmSelector == AlgorithmSelector.Multiply) {
            output = polymorphismCall(polymorphismDemoC, inputOne, inputTwo);
        }
        else if (algorithmSelector == AlgorithmSelector.Divide) {
            output = polymorphismCall(polymorphismDemoD, inputOne, inputTwo);
        }
    }

    function polymorphismCall(PolymorphismDemoA instance, uint inputOne, uint inputTwo) internal pure returns (uint output) {
        // it is determined which function is called only when below code line being executed.
        return instance.vfunc(inputOne, inputTwo);
    }
}