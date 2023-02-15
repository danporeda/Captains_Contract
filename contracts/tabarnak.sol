pragma solidity ^0.5.0;

contract TeamLedger{

    // Sub payments will all go into the teamPool, to be redistributed to full-time players at the end of the season.
    // full-timers missing a game will incur a weight of 1 in "gamesMissed" for redistribution claims. 
    uint public teamPool;

    // Full time Players will be registered with $560 amountPaid, which will be deducted from leagueFee.
    uint public leagueFee = 8400;

    struct Player{
        string name;
        string status;
        uint amountPaid;
        uint gamesPlayed;
        uint gamesMissed;
    }

    Player[] public team;

    struct Game {
        string date;
        string opponent;
        string players_out;
        string players_sub;
    }

    Game[] public games;

    event _Payment(string name, uint amount, string date);

    function registerPlayer(string memory name, string memory status, uint amount, string memory date) public {
        Player memory newPlayer = Player(name, status, amount, 0, 0);
        team.push(newPlayer);
        if (keccak256(abi.encodePacked(status)) == keccak256(abi.encodePacked("full time")) || keccak256(abi.encodePacked(status)) == keccak256(abi.encodePacked("part time")))
            {leagueFee -= amount;
            emit _Payment(name, amount, date);}
    }

    function subGame(string memory name, uint amount, uint position, string memory date) public {
        team[position].gamesPlayed += 1;
        if (amount > 0)
            {emit _Payment(name, amount, date);
            team[position].amountPaid += amount;
            teamPool += amount;}
    }

    function missedGame(uint position) public {
        team[position].gamesMissed += 1;
    }

    function gameRecord(string memory _date, string memory _opponent, string memory _players_out, string memory _players_sub) public {
        games.push(Game(_date, _opponent, _players_out, _players_sub));
        }

    
    function teamLength() public view returns (uint256) {
        return team.length;

    }
    function getPlayer(uint position) public view returns(string memory, string memory, uint, uint, uint) {
        return (team[position].name,
        team[position].status,
        team[position].amountPaid,
        team[position].gamesPlayed,
        team[position].gamesMissed);
    }

    function game_list_length() public view returns (uint) {
        return games.length;
    }

}