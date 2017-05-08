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

    let command = '%! echo Hello Word ' .g:sqlquery 
    exec command	

endfunction
