\documentclass[a4paper]{article}

\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage{algorithm}
\usepackage{algorithmicx}
\usepackage[noend]{algpseudocode}

\title{SBR Algorithm: Psaudo-code}

\author{Gal kaminka \& Shachar Sirotkin}

\date{\today}

\begin{document}
\maketitle

\section{CSQ}

\begin{algorithm}
\caption{CSQ(Matching set M, Library L, Time Stamp t}\label{alg:csq}
\begin{algorithmic}[1]
\ForAll{$v \in M$}
\State PropagateUp(v,L,t)
\EndFor
\ForAll{$v \in M$}
\While{$(tagged(v,t)) \land (\not\exists ChildTagged(t))$}
\State $delete_tag(v,t)$
\State $v \gets parent(v)$ 
\EndWhile\label{DeletePropagateDownWhile}
\EndFor
\end{algorithmic}
\end{algorithm}

\begin{algorithm}
\caption{PropagateUp(Node v, Library L, Time Stamp t)}\label{alg:propageteUP}
\begin{algorithmic}[1]
\State $Tagged \gets \emptyset$
\State PropagateUp(v,L,t)
\ForAll{$v \in M$}
\While{$(tagged(v,t)) \land (\not\exists ChildTagged(t))$}
\State $delete_tag(v,t)$
\State $v \gets parent(v)$ 
\EndWhile
\EndFor
\end{algorithmic}
\end{algorithm}

\end{document}
