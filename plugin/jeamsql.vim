" Check if jeamsql is loaded otherwise load it
if exists('g:loaded_jeamsql')
  finish
endif
let g:loaded_jeamsql = 1

" nnoremap <leader>se "ay :call jeamsql#JeamSQL()<CR>
" nnoremap <buffer> <leader>se "ay :call jeamsql#JeamSQL()<CR>
map <leader>se "ay:call jeamsql#JeamSQL()<CR>
