# nat

nat is a toy and experimental tool to execute terminal commands using natural language powered by ChatGPT (gpt-3.5-turbo). nat removes manual typing and memorizing complex command structures. 

<div align="center"><img src="https://i.gyazo.com/9700585203a78335e956ae4c2a715c8d.png"></div>

## Install

```
pip install git+https://github.com/minaminao/nat.git
```

## Usage

```
export OPENAI_API_KEY=<your key>
```

```
$ nat "Output Hello World"
(x) echo "Hello World" (Enter|↑|↓)
( ) printf "Hello World"
( ) echo -n "Hello"; echo " World"

Hello World
```

```
$ nat "1 + 2 + 3"
(x) echo $((1+2+3)) (Enter|↑|↓)
( ) expr 1 + 2 + 3
( ) bc -l <<< "1 + 2 + 3"

6
```

```
$ nat "Replace abc with def in a.txt"
(x) sed -i 's/abc/def/g' a.txt (Enter|↑|↓)
( ) awk '{gsub(/abc/, "def")}1' a.txt > temp.txt; mv temp.txt a.txt
( ) perl -pi -e 's/abc/def/g' a.txt
```

```
$ nat "fizzbuzz in bash"
(x) for i in {1..100}; do if (($i%15==0)); then echo "FizzBuzz"; elif (($i%3==0)); then echo "Fizz"; elif (($i%5==0)); then echo "Buzz"; else echo $i; fi; done (Enter|↑|↓)
( ) seq 1 100 | awk '{if($0%15==0) print "FizzBuzz"; else if($0%3==0) print "Fizz"; else if($0%5==0) print "Buzz"; else print $0}'
( ) for i in {1..100}; do echo -n "$i "; ((i%3==0)) && echo -n 'Fizz'; ((i%5==0)) && echo -n 'Buzz'; echo ""; done

1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz

(snip)
```