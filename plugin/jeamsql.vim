if exists("g:loaded_jeamsql")
    finish
endif

let g:loaded_jeamsql = 1

if !exists("g:jeamsql")
    let g:jeamsql = 1
endif

function! s:ExecuteSQL()
    
    
    let g:sqlquery =  @q

    if g:sqlauery == ""
        return 0
    endif


    if exists("g:running_buffer")
        " Go to buffer
        set swb = usetab
        exec "rightbelow sbuf " . g:running_buffer
    else
        bo new
        set buftype = nofile
        let g:running_buffer = bufnr("%")
    endif

    let command = '%! echo Hello Word ' . g:sqlauery 
    exec command

endfunction

nnoremap <leader>se :call jeamsql#ExecuteSQL()<CR>
nnoremap <buffer> <leader>se :call jeamsql#ExecuteSQL()<CR>
