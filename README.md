# nat

nat is a toy and experimental tool that enables seamless command execution using natural language powered by ChatGPT. nat removes the need for manual typing and memorizing complex command structures. 

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
