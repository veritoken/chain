pragma solidity ^0.4.21;

contract Greeter {
    string public greeting = 'Hello';

    function setGreeting(string _greeting) public {
        emit Greeting(greeting = _greeting);
    }

    function greet() view public returns (string) {
        return greeting;
    }

    event Greeting(string _greeting);
}
