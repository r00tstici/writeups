# Secure login - angstromctf

- Category: pwn
- Points: 50
- Solves: 334
- Solved by: Dovah

## Description

My login is, potentially, and I don't say this lightly, if you know me you know that's the truth, it's truly, and no this isn't snake oil, this is, no joke, the most secure login service in the world



Look into how strcmp works and how that fits in with what /dev/urandom returns.

## Solution

We are given an ultra secure login service. 

This time the service requires a random password at each login, generated using urandom:


```C
void generate_password() {

	FILE *file = fopen("/dev/urandom","r");
	fgets(password, 128, file);
	fclose(file);
}
```

Pretty solid: no one can guess a password if it's random and different at each login.

cclloooooooddoooooooooooooooooooooooooooooooooolooooooollllllllllllllllllllllooollllllc;:clllllllllllllllllllllllllllllllllllllllllllllllllllc,''',,;;
ccloooooodddddddddddoooodooooodddoooooooooooooooooooooooooooooooooooooooooooooooooooool::lllooooooooooooooooooooooooooooooooooooooollloooooool;,',,;;:
cclllooodddddddddddddddddddddddddoooooooooooooooooooooooooooooooooooooooooooooooooooool::llooooooooooooooooooooooooooooooooooooooooooooooooool;,',,;;:
:::clodddddddddddddddddddddddddddodooddddooooodddooddooooooooooooooddoooooooooodooooool::llooooooooooooooooooooooooooooooooooooooooooooooooooo:,'',;;:
:;:clloddxddxdddddddddddddddddddddddddddddddddddddodddoooooooodddddddddddddddddddooooooc:clooooooooooooooooooooooooooooooooooooooooooooooooooo:,'',;;:
cllolllodddddxddddxxddddddddddddddddddddddddddddddddddddoddddddddddddddddddddddddooooooc;cloooooooooooooooooooooooooooooooooooooooooooooooooooc,'',;;:
lloollcccclodxxxdxxddddddddddxxxddddddddddddddddollllcc::;;;:::::::cllllooddddddddoooooc;cloooooooooooooooooooooooooooooooooooooooooooooooooooc,'',;;;
ollccc::cccodxdddddddxxxxdddxxxxddxxxdddddddolc:;,,,''''..'''.........''',,;;:lodooooooc;cloooooooooooooooooooooooooooooooooooooooooooooooooooc;,',;;;
ooooolcllccooooddddddxxxxdddxxxxxxdxxxddol:;,,,''''..''........................',;cloool;:loooooooooooooooooooooooooooooooooooooooooooooooooool;,',;;;
oooollllllodllllodddxxxxxxddxxxxxxxddoc:;,'''''.....'.......................    ...':lol::loooooooooooooooooooooooooooooooooooooooooooooooooool;,',,;;
dddddooodxxdoc::oddxxxxxl;;::ccllooc:;,,,'.......................                   .'cl::loooooooooooooooooooooooooooooooooooooooloooooooooooo:,',,;;
dddddddddxxxdc;coddxxxd:.......',,,,,'''..................                            .;::loooooooooooooooooooooooooooooooooooooooolloooooooooo:,',,,;
dddddoodddxdl;';ccoddc,......',,,'''''........  ...                                    ..;looooooooooooooooooooooooooooooooooooooooooooooooooooc,',,;;
dddllc:;;:ll:'.''',,'.......',,'''.........                                              .;oooooooooooooooooooooooooooooooooooollooooooooooooooc,'',;;
cl:,''''',,'...............',,..... . .....                           ................''...coooooooooooooooooooooooooooooooooolllloooooooooooooc;'',,;
,,,'''.......'..'.........','......  .....      .....',,,''',,,,,,,,:cllccc::;;;,,'''',,,,.,loooooooooooooooooooooollooooooooolllloooooooooooool;,,,,;
''''''....................''........ ..       .,cloodxxxxxxxxxxxxxddxxxddddoolcc:;,,,,,,,,,,:looooooooooooooooooooollooooooooooollolllololloolol:,,',;
,,;,..''...',.............'...... .....     .,lxkkOOOOOOOOOOkkkkkxxxxxxdddddddolc:;;,,,,,;;,;clooooooooooooooooooolllooolllllllllllllllllllollol:,,,,;
:,'...,,................''......   .      .,lxkOOOOOOOOOkkkkkkkkkxxxxxddddddddoolc:;;;;;;;;,,,:looooooooooooolllllllloolllllllllllllllllllllllll:,,,,;
....','.................'....... ...... ..,:oxkkkkkkkkkkkkkkxxxxxxxxxdddddddddoolcc:;;;;;;;,,,,:loooooooooolllllllllloolllllllllllllllllllllllloc,,,,,
''''';;,','.............'....''....'''',;:cloxxkxkxxxxxxxxxxxxxxxxxxxddddddooooollcc:;;;;;;,,,'':ooooolloolllllollllllllllllllllllllllllllllllloc;'',,
,;;,,:lllcc,................';:;;:ccclllcclloodxxxxxxdddddddddddddddddooooooooooollc::;;;,,,,'''':oooooooolllllllllllllllllllllllllllllllllllllol;,'',
.'''.':lllc,.....................',,,,,',,;:cclooodddoooooooooooooooooooooooooolllllc:;;;;,,,'''.,cooloolllllllllllllllllllllllllllllllllllllllll;,,',
',,',,',,;;,...............      ........,,;;:cclooooolllllllooooooooooooooooollllllc::;;;;;;,,''';loooolllllllllllllllllllllllllllllllllllllllll:,,',
,;:;;:;'',;;'..............       .....',,;;;::clllllccccccllllllooooooooooooooooollcc:;;;;;;;,,,,,:loooollllllllllllllllllllllllllllllllllllllll:,'',
,,;;:cc;,;,''..............     .......,,,,;;;:cccccc::::ccccclllloooooooooooollllccc::;;;;:;;;,,;;'.,lolllllllllllllllllllllllllllllllllllllllll:,,',
,;cl:,;c:,,,................   ......'''',,,cx00kl:::::::ccccccllloooodddddddoollccc:::;;;;;;,,,,'.. .:ololllllllllllllllllllllllllllllllllllllllc,,,,
.';;,'';c:;,............  ..  ......'',,;:ldkOkkx:',;;;:ccllloodddddxxxxxdddddolccc::;;;;;;,''...    .colllllllllllllllllllllllllllllllllllllllllc;,,'
......',;;;,.............  ....','.'',;cdkOkxdoc,..',;:clodxxkkxdddooolllcccc:::;;;;;,,,,''...       'lollllllllllllllllllllllllllllllllllllllllll;,,'
,,,,''',;:c:'..................','',,;okOkdoc:;.. ..,;:clodddoc:;,,'.......    ......'''....         'clllllllllllllllllllllllllllllllllllllllllll;,,,
;,'.'''';cc:,...............',,;'.',cxkkkxl;'''....',;:cllc::;,,'.......            .......     .;;..':lllllllllllllllllllllllllllllllllllllllllll:,,,
.......';clc,.............'codddc;:dxxxdol:;,',,...',;:cc:;;,,,,''.......           ...,,'.     .::..:llllllllllllllllllllllllllllllllllllllllllll:,,'
.......',lxdc'............,;.',:oxxddoc::;;:;;;,,''',::;;'''''...    .  .          ..,:lol;.......  ..collllllllllllllllllllllllllllllllllllllllll:,''
.........,:l:'............,..,cldxolcc;;,,;;::::;;,,;;,''....          .c:'...  ...,;codxxdc'..... ...,cllllllllllllllllllllllllllllllllllllllllllc,''
.........................':,':ddddollc::::::ccc::;;;;,'............'...,:;'.....,;::clddxkxxl;'...''',';llllllllllllllllllllllllllllllllllllllllllc,''
..........................,,,cdxddoooc::lolcccc::::::,',,;;;::::;;;:;;,'......':lllloddxxkkkxl:;,'',,,,,:lllllllllllllllllllllllllllllllllllllllllc;''
...........................,;ldxxddol:;:odlcccc:clolc;,;;;:::::;,'.........',:clooodddxxxkkOOxolc:;,'''',cllllllllllllllllllllllllllllllllllllllllc;''
.....'''''''................;ldxxdolc;,;loc::::ckK0xl;;;;;:::ccccc:::;;;::cllooooooooddxkOO0OOxdlclc,...'cllllllllllllllllllllllllllllllllllllllllc;,'
..''''''',''''..............':dxdolc:,,;cl:;::cdOkddllccc:;,;coddxxxddooooooooc:;:codxxkkOOOOOkdlc;,'...'cllllllllllllllllllllllllllllllllllllllllc:''
''',,,;;;:,''''..............'oxoolcc;,,coo::codooooooolcc:'.':ldxkxxddoollcc;',;cldkkkkkxxxdolc:,...  .;llllllllllllllllllllllllllllllllllllllllll:,'
'''',,:ccc;'''...............'oxdollcc::coollloooooollc::;;,..':cllollcc:;,,'',;,',:cc:;,,''......     .clllllllllllllllllllllllllllllllllllllcclcl:,'
''''',,;;,,''..............'':xxddodxxddolclllllllcccccccccllccc:;,,,,,''.....',,'...                  'llllllllllllllllllllllllllllllllllllllcccccc,'
'''''',,,;,''...............'oxxddxxxxddlclodxxdolccllllloooooolc;'...........',;;,.                  .;lllllllllllllllllllllllllllllllllllllllllllc;'
'''''',;;:;''.............  'ooodddllloooodxkkkxdooooddoolcccccccc::;,..  ...'','...       ......... .,lllllllllllllllllllllllllllllcllllllllllllllc;,
'''''';:cc;''....''.......  'llloooc:cclloddddddodxxkkkxdl:;;::clllc:;,. .........     ...,,,,.......;clllllllllllllllllllllllllllllllcllllllllllllc;,
;;;:::ccllc:c:'.';,,'.....  .clllollc::ccloooollooddddddol:;;:ccccc:;,'.        ....',,,;;,.......'';llllllllllllllllllllllllllllllllccccccccccccccc:'
cllolll:::clol,..''''.....  .:llooollccccclooollooooollllc:;:ccc:;,'..'.         ...''........';::;;clllllllllllllllllllllllcccccccccccccccccccccccc:'
'.';;;,.',,,;,...........   .coooooollcccloooooooooollc::::::cllc;'..',.    ........',:clollccccc;,;lllllllllllllllllllllllllccccccclllccccccccccccc:,
.   ....';'...........     .:oooodoollllllooooooddoolcc:;;:::clooc'.,;'        .....'',;;::;;,''..'clllllllllllllllllccccccccccccccccccccccccccccccc:,
.     ................    .lxdolloollllllloooodddooolcc:::::;::cc;..''.              .........   .;llllllllllllclllccccccccclcccccccccccccccccccccccc;
......................   .okkdoolllllllllloolooooooollc::::::::;,',:,.                           .clllllllllllllccclccccccccccccccccccccccccccllccccc;
.',,,,,,;;;;;;,;,,,,,'..,dkkkxoloollclllllllllooooollccccc:::::;,,,'.                            ,llllllllllllcllccccccccclccccccccccccccccccclcccccc;
','',,,,,,,'''''''''',:ldkkkkxolllllcllllllllllllllllcccccc::::;;,.                             .:llllccllllllllllccccclllllccccccccccllcccccclllcccc:
'''.'''.............'cloxxxkkkdlllllcllllllllllllllllccllllc:::;;,.                             .',;:cclllllllllccccccccccccccccccccccclcccccllllcccc:
..    .           ..clcoodddxxxoccllllllllllllllllllcccllllcc::;,,.                             ......',;;::ccclcccccccccccccccccccccccccccccclllcccc:
               ..,;loccoldddddxdlccllllllllllllllllccllllllccc:;,,.                              ...........'',,,;;:ccccccccccccccccccccccccccccccccc:
           ..,:::ccoo:clcoddddddocccllllclllllllllcccclllllc:::;,'.                              ....................',;:ccccccccccccccccccccccccccccc
          .'col:,.'ll;cc:loddddddlccllllccccccllllccccclllcc::;,'..                               .  .........''.........',;:ccccccccccccccccccccccccc
        .':dxxdc'..::,::;cloddddddlccllccccccclllllllccccc:::;;'..                              .    .........''''...........',;::cccccccccccccccccccc
      .,:lddoolc;'.;:';,,:clloooddollllcccccccllllllllcccc:::;,'..                              .    ........'',''...............',;:ccccccccccccccccc
 ....,coodoccccllc::,';,';:ccllllolllllcccccllllolllolccc:::;,,'..                               .   ......''''','..'''..............',:cccccccccccccc
;::::;:lddoc;;:cccol'';',;:ccclllllllllcclllllooolooolcc:::;;,'...                  .......      ..   ......',''',''''''''..............';:ccccccccccc
looollc::::c:;,,,;cc.',',::cccllllooolllllllooooooodoolc::;;;,'..    .................'.....     ..   .......''',,,,,'',,,,................,;:cccccccc
:clloool:,'''''...;:.''.,;:ccccclloooooooooooodddddddolcc:;,,'...  ..................'......     ...   .......''',,,,,,',,;'.................':ccccccl
,,;:clooc;,''''...,,....,;:cc::ccloddxxdxxddddddddddddol:;,'.......................''.......    .....  ........'',,,,,,,,','..'................,:c:ccc
;:;;;;cc:;,'''''..;'....',:ccccccldxkkkkkOOOkxxxxdddddoc:,'.......................''........   ...'...  .........'''',,,',,'..''............. ...;:ccc
..,;:;,,'''''''''';'.....,;::::::okkO0000OKKO00KOOOkkxol:,,'....................','.........    ..'...............''''''''',,'.''............  ...,:::
'....;c:;,'.......,:.....',;;,'..oOk0KKKK0XKOKK0000OOkdoc;;;,,'..............'''''''''......   .........     ..................'''.'.........  ....,::
,'... .,clc:;'.......      .    .dkk0K00OON0OX0OKOO0kkdlc;;,;;,..........'''''''''''''''.....  ....... .                   .  .'..','.........  ....';
::;,..  .,cllc:;;,'''.....      ,xkkKKKK00N0OK0OOOOOkxdlc;;,;;,. ....''',,,,;,',,,,,'''''....  ............  ....    ..  ..'.....'',,.  ......   ....'
:ccc:;..  .;cllccc:;'...........:O00KKXX0OKOkxkkdxdoocc:,''',,.    ..',;:;',,,,;,;,,,,,,'''..  ..... ... ........   ......',.....'',,. ... ...    ....
;::c::;'.  .':cccc:,......''....c0XXKKKKxllc;.''',,,,'.........    .,:coo:,,,,,;;;;;;,,,,,''.  ...   .......'....   ..'...',. ....',,.  .   ..     ...


The problem here lies in the fact that a string-compare, strcmp(input, password), is used to validate the input. 
Since strcmp ceases the comparison whenever a character in a string reach the null byte, it can happen that the random password
generated using urandom begin with the null byte. 
The following extremely articulated and convoluted code gets the job done. 

```bash
for i in {1..100}; do (echo -ne "\x00" | ./login &) ;  done
```

(one shot one kill, no luck just skill)


