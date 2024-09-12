# Captain's Contract
## Smart Contract for management of sports teams.

### About
I created this app to manage my hockey team on-chain. It is currently functional but under development. The first release is a record of roster and payments, as a tool to keep track of atttendance and balances, essentially transactions to mutate state. Payments are made off-chain in USD through conventional routes, and these are recorded on-chain by the Captain/contract owner. 

### Features
- **Roster**: Players are added to the team roster as full-time or part-time status.
- **Payments**: All payments go to the teamPool. Full-time players register with a fixed fee, and part-timers submit payments with each game attended. At the end of the season, if there is a surplus balance in the teamPool, it is redistributed to full-time players.
- **Attendance**: `game_played` applies to part-timers, and `games-missed` to full-timers.


## Features To Come
- **payment transactions**: Currently there are no payment transactions in the contract as a matter of practicality; nobody on my team used crypto payments, and the league only accepted USD when I deployed the first contract. Future versions will enable team fees to be paid in USDC to the contract, retrievable to the owner or reditributed to external addresses by the owner.
