" Numbers
syntax match casoNumber "\d\+\(\.\d*\)\?"

" Types
syntax keyword casoType Int Float Bool List Str Any Empty

" Keywords
syntax keyword casoKeyword let const when fnc if else elsif loop to use obj init

" Boolean values
syntax keyword casoBoolean true false

" Operators
syntax match casoOperator "==\|!=\|<\|<=\|>\|>=\|?\|&&\|\|\|=\|:=\|:\|->\|@\|\|\|\.\|,\|;\|!"

" Arithmetic Operators
syntax match casoArithmetic "[+\-*/%]"

" Comments
syntax match casoComment "//.*$"

" Remove or comment out the identifier matching and highlighting, remove comment if you also want IDs to be highlighted
" syntax match casoIdentifier "[A-Za-z0-9_]\+" 

" Linking to predefined highlight groups
hi def link casoNumber Number
hi def link casoType Type
hi def link casoKeyword Keyword
hi def link casoBoolean Boolean
hi def link casoOperator Operator
hi def link casoArithmetic Statement
hi def link casoComment Comment
" hi def link casoIdentifier Identifier, remove comment if you also want IDs to be highlighted