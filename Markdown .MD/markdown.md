`These are the commands available to use`
`First off, install in VS the Auto-open preview markdown 

https://www.freecodecamp.org/news/markdown-cheat-sheet/`

TASK	MARKDWN SYNTAX

Heading 1	    #

Heading 2	    ##

Heading 3	    ###

Italics	        *italics*

Bold	        **Bold**

Strike	        ~~insert text~~

Block quote	    >

Links	        [link name](link.com)

Unordered list	* List item * List item

Code Block	    `insert code here`

With this you can create README.MD files....

# EXAMPLE README.MD

`these are real code blocks here!...`

## bla bla bla
* 1
* 2
* 3
 > bla bla bla

 **bla bla bla**

etc... [www.google.com] (www.google.com)
________________
________________
________________


https://www.freecodecamp.org/news/diagrams-as-code-with-mermaid-github-and-vs-code/

# Graphicals:

TYPE	DESCRIPTION

<|--	Inheritance

*--	    Composition

o--	    Aggregation

-->	    Association

--	    Link (Solid)

..>	    Dependency

..|>	Realization
..	Link (Dashed)

# EXAMPLE 1 
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

# Example 2
::: mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
:::

# Pie graph
::: mermaid
pie
    "whole" : 100
    "X" : 20
    "Y" : 75
    "rest" : 05
:::

# Flow chart
``` mermaid
flowchart TD;
    A[Start] --> B[Process 1];
    B --> C[Process 2];
    C --> D[End];
```

# Sequence driagram

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Register user
    activate Server
    Server-->>Client: User already exists.
    deactivate Server

```

# Class' diagram
```mermaid
classDiagram
    class Animal {
        +name: string
        +age: int
        +makeSound(): void
    }

    class Dog {
        +breed: string
        +bark(): void
    }

    class Cat {
        +color: string
        +meow(): void
    }

    Animal <|-- Dog
    Animal <|-- Cat
```

# Gantt
```mermaid
gantt
    title Project Schedule
    dateFormat YYYY-MM-DD
    axisFormat %m/%d

    section Planning
    Define Project : 2023-01-01, 7d
    Research : 2023-01-08, 14d
    Define Requirements : 2023-01-22, 7d

    section Development
    Design : 2023-01-29, 21d
    Implementation : 2023-02-19, 28d

    section Testing
    Unit Testing : 2023-03-19, 14d
    Integration Testing : 2023-04-02, 14d

    section Deployment
    Deploy : 2023-04-16, 7d
    User Training : 2023-04-23, 14d

    section Maintenance
    Ongoing Support : 2023-05-07, 30d
```

