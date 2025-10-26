% This LaTeX class file implements the Mads Føk Document Class.

% By Palle Joergensen 2003 <palle@pallej.dk>
% By Jonas 'Sortie' Termansen 2012, 2013, 2014 <sortie@cs.au.dk>, <sortie@maxsi.org>

% Greetings! This is the LaTeX system as passed down to you from your elders.
% You have been chosen to suffer through the undocumented and poorly
% implemented hacks in this file. Hey, it was much worse when I got here. At
% least I cleaned it up and attempted to document it.

% TODO: Revise this document class and try to document what the various code
% fragments do and confirm whether the comments are actually true.

% Specify the needed LaTex version.
% TODO: Optionally add a date, if it ever becomes a problem
\NeedsTeXFormat{LaTeX2e}

% Increment this value whenever you feel like making changes.
\ProvidesClass{MadsFoek}[2019/04/27 v. 1.7.1 Class for Mads Foek]

% Select the class that we extend.
% TODO: Shouldn't we be using memoir instead of article?
% NOTE: There bee missing fonts on memoir
\LoadClass[twoside,a5paper]{article}
%\PassOptionsToClass{}{article}
% TODO: Figure out what packages are provided by our base document class, so we
% don't have to include then here.

% Select the One True Encoding: UTF-8.
\RequirePackage[utf8]{inputenc}

% Specify the dimensions of our magazine.
\RequirePackage[a5paper,twoside,%
     left=1cm,right=1.5cm,%
     top=1cm,bottom=1.5cm,marginparwidth=0cm,marginparsep=3mm,%
     includemp=true,%
]{geometry}

% Package that allows conditionals.
\RequirePackage{ifthen}

% Package that allows splitting words.
\RequirePackage{babel}

% Package that allows inserting images and other graphics.
\RequirePackage{graphicx}

% dvips:  Used for insertion of Compressed EPS and non-EPS graphic formats like
%         TIFF, GIF, JPEG ...
% pdftex: Allows additional options to be used with includegraphics, when the
%         document is compiled with pdflatex (which the current Makefile does
%         2019/04/25)
% draft:  Should render all pictures as bounding boxes with titles; pictures
%         dissapear when this option is removed.
% final:  Should render all pictures as pictures
\PassOptionsToPackage{dvips,pdftex,draft,final}{graphicx}

% TODO: What does this do and is that what we want?
% Package which allows placement of boxes at absolute positions in a LaTeX
% page
%
% absolute: makes all positions use a default anchor, making it possible to
%           create a rigirous layout.
% overlay:  The layout defined overlays other page elements
\RequirePackage[absolute,overlay]{textpos}

% Package that allows writing in multiple columns.
\RequirePackage{multicol}

% Package that allows inserting URLs.
\RequirePackage{url}

% Package that helps counter macros that eat whitespace.
\RequirePackage{xspace}

% Package that allows for customizing the Table Of Contents, table of figures,
%   etc..
\RequirePackage{tocloft}

% Allows for more control about how a hline should be drawn with the hhline
%   command
\RequirePackage{hhline}

% Allows for custom comments
% TODO check usage
\RequirePackage{comment}

% Allows for setting foreground and background colors
% NOTE: I can't imagine we use this -Erik Funder
\RequirePackage{color}

% Provides tables which automatically resizes their coloums to fit their
%   environment.
\RequirePackage{tabularx}

% Package that provides various math symbols.
\RequirePackage{amssymb}

% Package that provides various math things.
\RequirePackage{amsmath}

% Package that provides aditional fonts like \mathbb
\RequirePackage{amsfonts}

% TODO: Currently isn't used, should make it possible to write paragraphs in
%   different forms (like polygons)
%\RequirePackage{shapepar}

% TODO: What does this do?
\RequirePackage{palatino}

% TODO: What does this do?
\RequirePackage{mathpazo}

% TODO: What does this do?
\RequirePackage[perpage]{footmisc}

% TODO: What does this do? (Many includes at once?)
\RequirePackage{wrapfig,fame,fancybox,booktabs}

% Package that provides striked out text (\cancel).
\RequirePackage{cancel}

% Generate lorel ipsum filler text.
\RequirePackage{lipsum}

% For the sout command to do strike-through text. Normalem to not change the
% emphasis to be underlined (rather than the desirable default italic).
\RequirePackage[normalem]{ulem}

% Package that provides more compact enumerate environements using
% the [itemsep=foo] syntax.
\RequirePackage{enumitem}

% For justifying the text to the right margin to avoid ragged lines.
\RequirePackage{ragged2e} 

% For including raw PDFs using \includepdf.
\RequirePackage{pdfpages}

% TODO: Something to do with under the tables of contents.
\newboolean{undertoc}
\setboolean{undertoc}{true}
\DeclareOption{noundertoc}{\setboolean{undertoc}{false}}

% TODO: Numbers in calendar or what is this?
\newboolean{numbercal}
\DeclareOption{numbercal}{\setboolean{numbercal}{true}}

% TODO: What does this do?
\ProcessOptions

% Prefer some greek letters.
% TODO: Do we actually want these (yay, religious war) and shouldn't we swap the
% macros at least?
\let\epsilon\varepsilon
\let\theta\vartheta
\let\phi\varphi

% Set the right font sizes. TODO: Do we need to do this and do we do this in the
% correct manner?
\renewcommand{\tiny}{\fontsize{5}{7}\selectfont}
\renewcommand{\scriptsize}{\fontsize{5}{7}\selectfont}
\renewcommand{\footnotesize}{\fontsize{6}{8}\selectfont}
\renewcommand{\small}{\fontsize{7}{9}\selectfont}
\renewcommand{\normalsize}{\fontsize{8}{10}\selectfont}
\renewcommand{\large}{\fontsize{10}{12}\selectfont}
\renewcommand{\Large}{\fontsize{12}{14}\selectfont}
\renewcommand{\LARGE}{\fontsize{14}{16}\selectfont}
\renewcommand{\huge}{\fontsize{17}{19}\selectfont}
\renewcommand{\Huge}{\fontsize{20}{22}\selectfont}

% Don't display section numbers.
\setcounter{secnumdepth}{0}

% Only show sections in table of contents.
\setcounter{tocdepth}{1}

% Store the volume, vintage, day, month and year of this release.
\newcounter{volume}
\setcounter{volume}{0}
\newcounter{vintage}
\setcounter{vintage}{0}

% Commands to change the volume/vintage/date of a release.
% TODO: Clean this up a bit?
\newcommand{\theday}{\the\day}
\newcommand{\theyear}{\the\year}
% TODO: Is this switch hacky or a good thing?
\newcommand{\themonth}{\ifcase\month\or januar\or februar\or marts\or
  april\or maj\or juni\or juli\or august\or september\or oktober\or
  november\or december\fi}
\def\thisday#1{\def\@day{#1}}
\thisday{\theday}
\def\thismonth#1{\def\@month{#1}}
\thismonth{\themonth}
\def\thisyear#1{\def\@year{#1}}
\thisyear{\theyear}
\newcommand{\thisvolume}[1]{\setcounter{volume}{#1}}
\newcommand{\thisvintage}[1]{\setcounter{vintage}{#1}}

% Shorthand macros occasionally used by people.
% TODO: Do we want these, possibly with other names, and in that case document
% them and actually use them!
\newcommand{\dat}[1]{\begin{flushright}{\bf #1}\end{flushright}}
\newcommand{\cit}[1]{\begin{quote}{\bf Hetz:}\\ #1\end{quote}}
\newcommand{\skrevetaf}[1]{\begin{flushright}{#1}\end{flushright}}

% These are the nice and friendly Mads Føk logo macros. We use \xspace such that
% you can just use \madsfoek in normal text without worrying about whitespace.
\def\@madsfoek{\includegraphics[height=2mm]{madsfoek.png}}
\def\@madsfoeks{\includegraphics[height=2mm]{madsfoeks.png}}
\def\m@ds{\includegraphics[height=2mm]{mads.png}}
\def\@foek{\includegraphics[height=2.5mm]{foek.png}}
\def\@foeks{\includegraphics[height=2.5mm]{foeks.png}}
\def\foek{\@foek\xspace}
\def\foeks{\@foeks\xspace}
\def\mads{\m@ds{}\xspace}
\def\madsfoek{\m@ds{}~\@foek\xspace}
\def\madsfoeks{\m@ds{}~\@foeks\xspace}

% These macros define the style of the footers and headers on each page.
% TODO: Does this do what we want it to?
\newcommand{\defaultfootstyle}[1]{\textbf{#1}}
\newcommand{\defaultheadstyle}[1]{\defaultfootstyle{#1}}
\newcommand{\artfootstyle}[1]{\defaultfootstyle{#1}}
\newcommand{\artheadstyle}[1]{\defaultheadstyle{#1}}

% TODO: These front page (fp*) commands are poorly named.
% Defines the style of the front page slogan.
\newcommand{\fpcomstyle}[1]{\texttt{\large #1}}

% Defines the style of the front page footer (date, volume, vintage).
\newcommand{\fpfootstyle}[1]{\defaultfootstyle{\large #1}}

% Set up footnotes.
% TODO: What exactly does this code do and how?
\newlength{\footnoterulelength}
\setlength{\footnoterulelength}{.4\textwidth}
\newlength{\footnoterulewidth}
\setlength{\footnoterulewidth}{.4pt}
\renewcommand\footnoterule{%
\hskip-\parindent\rule{\footnoterulelength}%
{\footnoterulewidth}\strut%
}

% TODO: What was it that this does?
\fboxsep0pt

% The @headmark variable contains the header of the current page. It is set
% using the \headmark{foo} macro. This is used by the foek pagestyle.
\let\@headmark\relax
\def\headmark#1{%
  \global\def\@headmark{#1}}

% The foek pagestyle displays page numbers as well as the headers and footers.
% TODO: Perhaps make this code more readable?
\newcommand{\ps@foek}{%
  \def\@evenhead{\raisebox{-3pt}{\rule{\textwidth}{.4pt}}\hskip-\textwidth%
    \artheadstyle{\@headmark}\hfill}%
  \def\@oddhead{\raisebox{-3pt}{\rule{\textwidth}{.4pt}}\hskip-\textwidth%
    \hfill\artheadstyle{\@headmark}}%e
  \def\@evenfoot{\artfootstyle{\madsfoek~side~\thepage\hfill}}%
  \def\@oddfoot{\artfootstyle{\hfill\madsfoek~side~\thepage}}%
}

% Customize the section command and center the title.
% TODO: This seems a bit hacky and should be examined.
\renewcommand\section{\@startsection {section}{1}{\z@}%
  {-3.5ex \@plus -1ex \@minus -.2ex}%
  {2.3ex \@plus.2ex}%
  {\normalfont\centering\Huge\bfseries}}

% Declare the table of contents macros
\renewcommand\tableofcontents{\@starttoc{toc}}
\renewcommand{\cfttoctitlefont}{\bfseries}
\renewcommand{\cftsecfont}{\normalfont}
\renewcommand{\cftsecpagefont}{\normalfont}
\setlength{\cftbeforesecskip}{.3mm}

% Remove the title over the table of contents. Doing it directly here doesn't
% seem to work, so we inject the command using his hack.
\AtBeginDocument{%
\renewcommand{\contentsname}{}%
}

% TODO: This is replaced by the below.
%% The abstract environment
%% TODO: Document this and make sure it works as intended. I think it implements
%% a short description before the real article starts.
%\newlength{\PJF@abstractwidth}
%\renewenvironment{abstract}{%
%  \noindent\hskip\parindent\begin{minipage}{\PJF@abstractwidth}%
%    \itshape%
%  }{%
%  \end{minipage}%
%}

\newlength{\PJF@abstractwidth}
\renewenvironment{abstract}{%
  \begin{center}%
  \itshape%
}{%
  \end{center}%
}

% The following commands inserts articles (artikeler), notices (opslag),
% cartoons (tegneserier) and such. The append version doesn't make a clean page
% while the normal version starts a new page.

% TODO: Is \InputIfFileExists the input method we want and can we improve the
% error mesage - and how about aborting the compile?

% TODO: The naming convention is a horrible mix of danish and english (yay).

% TODO: Clean this code up a bit?

% TODO: Make these commands more readable to use, so people have an easier time
% remembering them and such. Should part of these macros be moved into the file
% that they are including?

% Add an entry to table-of-contents and sets the page header.
\newcommand{\foekcontentslineheadmark}[2]{% header, toc
  \if #2*\relax\else
  \addcontentsline{toc}{section}{#2}
  \fi
  \if #1*\relax\else
  \headmark{#1}
  \fi
}

% An article in two columns.
\newenvironment{appendarticle}[4][@]{% [abstract], title, header, toc
  \foekcontentslineheadmark{#3}{#4}
  \begin{multicols}{2}[%
    \if #2*\relax\else
    \section*{#2}
    \fi
    \if #1@\relax\else
      \begin{abstract}
        #1
      \end{abstract}
    \fi
    ]%
    \noindent\ignorespaces%
}{%
  \end{multicols}
}

% An article in a single column.
\newenvironment{appendarticlesingle}[4][@]{% [abstract], title, header, toc
  \foekcontentslineheadmark{#3}{#4}
  \if #2*\relax\else
  \section*{#2}
  \fi
  \if #1@\relax\else
    \begin{abstract}
      #1
    \end{abstract}
  \fi
  \noindent\ignorespaces%
}{%
}

% An article in two columns on the next page.
\newenvironment{article}[4][@]{% [abstract], title, header, toc
  \clearpage
  \begin{appendarticle}[#1]{#2}{#3}{#4}
}{%
  \end{appendarticle}
}

% An article in a single column on the next page.
\newenvironment{articlesingle}[4][@]{% [abstract], title, header, toc
  \clearpage
  \begin{appendarticlesingle}[#1]{#2}{#3}{#4}
}{%
  \end{appendarticlesingle}
}

% Appends an article onto the current page. Articles are columized.
\newcommand{\appendartikel}[5][@]{% [abstract], title, header, toc, file
  \begin{appendarticle}[#1]{#2}{#3}{#4}
    \InputIfFileExists{#5}{\ignorespaces\noindent}%
    {\Large{\centering Fil ikke fundet: \texttt{#5}}\normalsize}
  \end{appendarticle}
}

% Inserts an article onto the next page.
\newcommand{\artikel}[5][@]{% [abstract], title, header, toc, file
  \clearpage
  \appendartikel[#1]{#2}{#3}{#4}{#5}
}

% Appends an opslag onto the current page. Opslag are in a single column.
\newcommand{\appendopslag}[5][@]{% [abstract], title, header, toc, file
  \begin{appendarticlesingle}[#1]{#2}{#3}{#4}
    \InputIfFileExists{#5}{\ignorespaces\noindent}%
    {\Large{\centering Fil ikke fundet: \texttt{#5}}\normalsize}
  \end{appendarticlesingle}
}

% Inserts an opslag onto the next page.
\newcommand{\opslag}[5][@]{% [abstract], title, header, toc, file
  \clearpage
  \appendopslag[#1]{#2}{#3}{#4}{#5}
}

% Inserts a cartoon on the next page.
\newcommand{\centercartoon}[5]%
           [width=\linewidth]{% [includegraphics options], graphic file, 
                              % header, toc,  something on the page 
                              % (e.g. hetzes)
  \clearpage
  \foekcontentslineheadmark{#3}{#4}
  \mbox{}\vfill
  \begin{center}\ignorespaces
    \includegraphics[#1]{#2}
  \end{center}
  \vfill
  #5}

% TODO: Perhaps these cartoon commands can be improved?

% Appends a cartoon on the current page.
\newcommand{\appendcartoon}[5]%
           [width=\linewidth]{% [includegraphics options], graphic file, 
                              % header, toc, something on the page 
                              % (e.g. hetzes)
  \foekcontentslineheadmark{#3}{#4}
  \begin{center}\ignorespaces
    \includegraphics[#1]{#2}
  \end{center}
  #5}

% Inserts a cartoon on the next page.
\newcommand{\cartoon}[5]%
             [width=\linewidth]{% [includegraphics options], graphic file,
                                % header, toc,  something on the page   
                                % (e.g. hetzes)
   \clearpage
   \appendcartoon[#1]{#2}{#3}{#4}{#5}
}

% The dampventilen section.
\newenvironment{dampventilen}{%
  \clearpage
  \foekcontentslineheadmark{Dampventilen}{Dampventilen}
  \includegraphics[width=1.0\textwidth]{dampventilen_header.png}
  %\vfill
  \begin{abstract}
    Velkommen til vores brevkasse ``Dampventilen''. Det er her, du lukker damp
    ud -- det være sig varm luft, skoldhed kritik eller hvis du bare må fortælle
    verden om de der fine nye lyserøde sko\ldots{} For at komme i damp-ventilen
    skal du bare sende en mail til \url{red@madsfoek.dk} med emne
    ``Dampventilen'', og medmindre der vil være direkte juridiske komplikationer
    ved at trykke dit bidrag vil din mening formentlig blive udbasuneret og
    proklameret i næste \foek.
  \end{abstract}
}

% An entry in te dampventilen section.
\newenvironment{damp}[2][@]{% [abstract], title
  \begin{multicols}{2}[%
    \section{#2}
    \if #1@\relax\else
      \begin{abstract}
        #1
      \end{abstract}
    \fi
    ]%
    \noindent\ignorespaces%
}{%
  \end{multicols}
}

% Inserts a blank page.
\newcommand{\blank}[2]{% header, toc
  \clearpage
  \if #2*\relax\else
  \addcontentsline{toc}{section}{#2}
  \fi
  \if #1*\relax\else
  \headmark{#1}
  \fi
  \mbox{}
}

% Select which logo to show on the front page.
\def\frontlogo#1{\def\@frontlogo{#1}}
\frontlogo{madsfoek.png}

% Inserts the logo onto the front page as in the logo.png file.
\newcommand{\PJFforsidegrafik}{\includegraphics[width=\linewidth]%
  {\@frontlogo}\bigskip\newline}

% Apologies for the following. The idea is that the slogan on the top of the
% front page should be in entirely capital letters with some spacing. To do that
% we have added \hfill{} between each letter, resulting in very unreadable code
% for setting the slogan. Instead, we now use the following _ugly_ hack to do
% this. It is pretty fragile as far as I recollect and it was a mix of stuff I
% found online and my own incompetence. The desired experience is simply using
% a macro in main.tex to set the slogan and some code handles reformatting it
% nicely (see previous releases of Mads Føk) with capital letters with some
% spacing.

% TODO: There is a bit of redundancy in these comments.
% TODO: Oh my god - my eyes. What code have past me written?!

% A variable that contains the slogan on the front page.
\def\fpcom#1{\def\@fpcom{#1}}
\fpcom{}

% Reads a character into the variable \char.
\def\popchar{\let\char= }

% A recursive command that adds \hfill{} between all characters in the input
% string. This is useful for the slogan on the front page. The recursive part of
% it adds \hfill{} until it reads the \nil macro, which terminates the loop.
\def\forkmixhfillrec{\afterassignment\forkmixhfillinner\popchar}
\def\forkmixhfillinner{%
  \ifx\char\nil \let\next=\relax%
  \else%
     \prefix\char%
     \let\prefix=\hfill{}%
     \let\next=\forkmixhfillrec%
  \fi%
  \next%
}
\newcommand{\forkmixhfill}[1]{%
  \let\prefix=\relax%
  \forkmixhfillrec #1\nil%
}

% Sets the slogan displayed on the front page. All characters in the slogan will
% be interspaced with \hfill{} to spread it out a bit. Remember that a good Mads
% Føk slogon is written in entirely capital letters.
\newcommand{\frontslogan}[1]{%
  \fpcom{\forkmixhfill{#1}}%
}

% Defines the forside page style.
% TODO: Perhaps clean this up and document it?
\newcommand{\ps@forside}{%
  % Insert a nice frontpage slogan at the top.
  \def\@oddhead{\hfil\fpcomstyle\@fpcom\hfil\hskip-1cm\bigskip}%
  \let\@evenhead\@oddhead%
  % At the button put some meta information.
  \def\@oddfoot{\fpfootstyle{\madsfoek{}~nr.~\thevolume%
    \hfill\thevintage.~\aa{}rgang\hfill%
    d.~\@day.~\@month~\@year\hskip-1cm}}%
  \let\@evenfoot\@oddfoot%
}

% Defines the forside environment.
% TODO: Are these margins what we want?
\newenvironment{forside}{%
  \setlength{\TPHorizModule}{1mm} 
  \setlength{\TPVertModule}{1mm}
  \geometry{marginparwidth=1cm} 
  \clearpage
  \thispagestyle{forside}
  \centering\vspace*{-10mm}
  \PJFforsidegrafik
    \begin{minipage}{\linewidth}}{\end{minipage}\clearpage%
  }

% TODO: What does this do?
\DeclareTextCommandDefault{\textellipsis}{%
  .\kern\fontdimen3\font
  .\kern\fontdimen3\font
  .}

% Import our hacky replacement for the TKET package to write TÅGEKAMMERET.
\input{TKETISH.tex}

% This defines the layout and content of the second page (the TOC).
% TODO: This table system is very fragile and explodes a bit when it overflows.
% Either we need more control or a way of telling LaTeX to what we desire.
% (The old solution, now deleted, was unspeakably bad. Let's just say lines were
% drawn manually with hard-coded coordinates.)
% TODO: Clean this up.
\newenvironment{side2}{
  \clearpage
  \addcontentsline{toc}{section}{Den har forsiden på bagsiden}
  \begin{tabular}{||p{11.5cm}||}
    \hhline{|t:=:t|}
    %\begin{raggedright}
    \\\input{side2.tex} \\
    %\end{raggedright} \\
    \hhline{|:=:|}
    \\\noindent\textbf{Indholdfortegnelse}
    \begin{multicols}{2}
      \tableofcontents
    \end{multicols} \\
    \hhline{|:=:|}
    \\
}{ \\ \\ % The list of people who made this release is put here (in main.tex).
    \hhline{|b:=:b|}
  \end{tabular}
  \clearpage
}

% This defines the layout of the back side calendar.
% TODO: Guess what. This is also very fragile and hacky, but slightly better
% than what it replaced.
\newenvironment{kalender}[4][width=12cm]{%
  \clearpage
  \thispagestyle{empty}
  \def\kalenderfigur{\includegraphics[#3]{#2}}
  \def\kalenderfigurtitle{#4}
  \begin{tabular}{||c||}
    \hhline{|t:=:t|}
    %\rule{0pt}{0.2mm} \\
    \Huge{Kalenderen} \\
    %\rule{0pt}{0.2mm} \\
    \hhline{|:=:|}
    \begin{tabular}{lp{7.5cm}}
      }{ % The events are inserted here.
    \end{tabular} \\
    \hhline{|:=:|}
    \rule{0pt}{1mm} \\
    \kalenderfigur \\
    \kalenderfigurtitle \\
    \rule{0pt}{1mm} \\
    \hhline{|b:=:b|}
  \end{tabular}
  \begin{flushright}
    \hfill{\footnotesize ISSN:~1399-8560}
  \end{flushright}
}


% And, at last: Dr. Føk!

% TODO: Clean up this API and give things better names.

\newcommand{\spgm}[3]{%
  \noindent\large\bfseries #1 \\\mdseries
  \noindent\normalsize\textit{Kære Dr. Føk.\\ #2\\}
  \vspace{-2mm}
  \begin{flushright}#3
  \end{flushright}}

\newcommand{\svar}[2]{\noindent Kære #1\\ #2 \\
  \vspace{-2mm}
  \begin{flushright}
    \itshape Dr. Føk
  \end{flushright}}

\newcommand{\drfoek}[5]{\spgm{#1}{#2}{#3} \svar{#4}{#5}}

% TODO: Oh god. A macro that includes a file and adds all sorts of stuff around
% it, is horrible code, very hacky, undocumented, plenty of hard-coded
% coordinates, and what not.
% TODO: Clean this up, split into a few macros, possibly even an environment.
\newcommand{\DrFoek}[1]{% file
  \clearpage
  \newlength{\PJFDMPW}
  \newlength{\PJFDPW}
  \setlength{\PJFDMPW}{\linewidth}
  \setlength{\PJFDPW}{45mm}
  \addtolength{\PJFDMPW}{-\PJFDPW}
  \addtolength{\PJFDMPW}{-4mm}
  \setlength\unitlength{1mm}
  \noindent
  \begin{picture}(200,32)
    \put(0,3){\includegraphics[width=\PJFDPW]%
      {DrFoekpic.png}}
    \put(0,0){\rule{\linewidth}{3pt}}
    \put(47.5,17){\begin{minipage}{\PJFDMPW}
        \parfillskip=0pt
        \fontsize{8pt}{10pt}\selectfont
        Spørg Dr.\ Føk er en brevkasse for alle læsere af Mads Føk.
        Dr.\ Føk har svar på alt mellem himmel og jord.  Indsend
        dine spørgsmål enten ved at aflevere det i Føks postkasse på
        Matematisk Informationskontor, eller 
        til \url{drfoek@madsfoek.dk}. Alle spørgsmål skal være
        forsynet med navn og adresse, men bringes under mærke her på
        siden.  Vi forbeholder os ret til at forkorte brevene.
      \end{minipage}}
%%
%%   Lidt fjolleri, der goer at der i nummer 0 bliver et Dr. Foek
%%   Classic i stedet for den alm. Dr Foek
%%   Den oprindelige kode er /vist nok/ den her:
%%      \put(59,34.2){\fontsize{22pt}{24pt}\selectfont\bfseries%
%%        Spørg Dr.\ Føk}%
%%    
%% <fjolleri>
    \ifthenelse{\equal{\value{volume}}{0}}{%
      \put(47,34.2){\fontsize{21pt}{23pt}\selectfont\bfseries%
        Spørg Dr.\ Føk Classic%
      }%
    }{%
      \put(59,34.2){\fontsize{21pt}{23pt}\selectfont\bfseries%
        Spørg Dr.\ Føk%
      }%
    }
%% </fjolleri>
%%
    % Ramme omkring billede    
    \put(0,3){\rule{\PJFDPW}{1pt}}
    \put(0,3){\rule{1pt}{.79\PJFDPW}}
    \put(0,38.5){\rule{\PJFDPW}{1pt}}
    \put(44.68,3){\rule{1pt}{.79\PJFDPW}}
% Ramme oomkring text
    \put(46.3,3){\rule{74.65mm}{1pt}}
    \put(46.3,3){\rule{1pt}{29mm}}
    \put(46.3,32){\rule{74.65mm}{1pt}}
    \put(120.6,3){\rule{1pt}{29mm}}
  \end{picture}
  \addcontentsline{toc}{section}{Dr.\ Føk}
  \headmark{Spørg Dr.\ Føk}
  \vspace{-5mm}
  \begin{multicols}{2}
  \InputIfFileExists{#1}{\ignorespaces\noindent}{%
    \begin{center}
      \Large Fil ikke fundet: \texttt{#1}      
    \end{center}%
  }
  \end{multicols}
}

% These are executed when the document is begun.
% TODO: And what does they do? Looks like they set some constants to the
% dimensions of the magazine. These should be gathed at some global point and
% controlled from a single place, or something.
\AtBeginDocument{%
\setlength{\TPHorizModule}{1mm}%
\setlength{\TPVertModule}{1mm}%
\setlength{\PJF@abstractwidth}{\textwidth}%
\addtolength{\PJF@abstractwidth}{-2\parindent}%
\pagestyle{foek}%
\frenchspacing%
\headmark{\textit{Empty header}}%
}

% Here's some Hetz magic!
% TODO: Yay, this inserts the hetz declarations (into the document class?!) as
% produced by the build system.
% \input hetz

% TODO: Oh - what the fuck is going on here with \hetzfile?
% TODO: Clean up the hetz API.

%\newwrite\hetzfile
%\immediate\openout\hetzfile\jobname.htz

%\makeatletter
%\def\hetz(#1,#2,#3)#4{%
%%%\rlap{%
%\begin{textblock}{100}(#1,#2)%
%\rotatebox{#3}{%
%\begin{minipage}{4cm}%
%\normalfont\small\textbf{Hetz:}\\ \hetztext{#4}%
%\end{minipage}%
%}%
%\end{textblock}%
%\write\hetzfile{Hetz #4 on page \thepage.}%
%%%}%
%}

%\def\hetzher#1{%
%\noindent\begin{minipage}{4cm}%
%\normalfont\small\textbf{Hetz:}\\ \hetztext{#1}\\%
%\write\hetzfile{Hetz #1 on page \thepage.}%
%\end{minipage}\\%
%}

%\def\hetzpageentry#1{%
%\noindent\begin{minipage}{4cm}%
%\normalfont\small\textbf{Hetz #1:}\\ \hetztext{#1}\\%
%\end{minipage}\\%
%}

%\def\hetzheromvendt#1{%
%\rotatebox{180}{%
%\noindent\begin{minipage}{4cm}%
%\normalfont\small\textbf{Hetz:}\\ \hetztext{#1}\\%
%\write\hetzfile{Hetz #1 on page \thepage.}%
%\end{minipage}\\%
%}}

%\makeatother

% Hats for reviews.
\newcommand{\helhat}{\ensuremath{%
  \mathchoice{\includegraphics[height=4ex]{helhat}}
    {\includegraphics[height=4ex]{helhat}}
    {\includegraphics[height=3ex]{helhat}}
    {\includegraphics[height=2ex]{helhat}}
}}

\newcommand{\tomhat}{\ensuremath{%
  \mathchoice{\includegraphics[height=4ex]{tomhat}}
    {\includegraphics[height=4ex]{tomhat}}
    {\includegraphics[height=3ex]{tomhat}}
    {\includegraphics[height=2ex]{tomhat}}
}}
\newcommand{\semihat}{\ensuremath{%
  \mathchoice{\includegraphics[height=4ex]{semihat}}
    {\includegraphics[height=4ex]{semihat}}
    {\includegraphics[height=3ex]{semihat}}
    {\includegraphics[height=2ex]{semihat}}
}}
