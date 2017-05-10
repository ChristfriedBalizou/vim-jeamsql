let g:jeamsqlinitfile = ".jeamsql.ini"

function! jeamsql#GetConnectionString()
    " Load database credential and configuration
    
    let delimiter = ";jms;"
    let str = "" 

    " Get connection string
    if exists("g:jeamsql_connection")
        return split(g:jeamsql_connection, delimiter)
    endif

    return []

endfunction 


function! jeamsql#CreateConfigFile()

    let config = jeamsql#GetConnectionString()

    if len(config) > 0
        
        silent! delete(g:jeamsqlinitfile)
        call writefile(config, g:jeamsqlinitfile)
    endif

endfunction

" Look for sql query
function! jeamsql#GetQuery() 

    " Store old register
    let g:old_reg = @a
    
    "Copy new text to register a
    normal! "ay

	" Get gv text
	let g:value = join(split(@a, "\n"), " ")
    
    " restore register value
    let @a = g:old_reg
	
	" If gv text is empty get cursor line text
	if g:value == ""
		let g:value = getline(".")
	endif
	
	" If line is empty get whole buffer
	if g:value == ""
		let g:value = bufnr("%")
	endif

	return g:value

endfunction


" SQL executor function
function! jeamsql#JeamSQL()
	
	let g:sqlquery = jeamsql#GetQuery()

	" If buffer empty then 'nothing to do'
	if g:sqlquery == ""
		return 0
	endif

	if exists("g:running_buffer")
		" Go to buffer
		silent! set swb=usetab
		exec "rightbelow sbuf " . g:running_buffer
    else
        bo new
        silent! set buftype=nofile
        let g:running_buffer = bufnr("%")
    endif

    " Create config file
    call jeamsql#CreateConfigFile()


    if !exists("g:jeamsql_config")
        echom "No config setted. Nothing to do."
        return 0
    endif


    " Execute command
    let g:jeams = "python ~/.vim/bundle/vim-jeamsql/python-jeamsql.git/app.py"
    exec '%!'.g:jeams.' -q "'.g:sqlquery.'" -d '.g:jeamsql_config.' -c "'.g:jeamsqlinitfile.'"'

    " Delete config file
    silent! delete(g:jeamsqlinitfile)

endfunction
