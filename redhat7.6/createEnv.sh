#!/bin/bash

function vimrc(){
    VIMRC=${HOME}"/.vimrc"
    ROOT_VIMRC="/root/.vimrc"
    touch $VIMRC
    echo "
    syntax on
    set nocompatible
    set backspace=indent,eol,start
    filetype plugin indent on
    syntax enable
    set clipboard=unnamed,autoselect
    set number
    set listchars=tab:^\ ,trail:~
    set expandtab
    set tabstop=4
    set softtabstop=4
    set shiftwidth=4
    set autoindent
    set ruler
    nnoremap <Esc><Esc> :nohlsearch<CR><ESC>
    set ttimeoutlen=10
    set hlsearch
    set ignorecase
    set smartcase
    set wildmenu
    set noundofile
    set nobackup
    set noswapfile
    set encoding=utf-8

    set statusline=%#LineNr#
    set statusline+=%F
    set statusline+=%#Cursor#
    set statusline+=\ %m
    set statusline+=%=
    set statusline+=%#CursorColumn#
    set statusline+=\ %{&fileencoding?&fileencoding:&encoding}
    set statusline+=\[%{&fileformat}\]
    set statusline+=\ %p%%
    set statusline+=\ %l:%c
    set laststatus=2

    if has("autocmd")
        filetype plugin on
        filetype indent on
        autocmd FileType c          setlocal sw=4 sts=4 ts=4 et
        autocmd FileType html       setlocal sw=2 sts=2 ts=2 et
        autocmd FileType ruby       setlocal sw=4 sts=4 ts=4 et
        autocmd FileType js         setlocal sw=4 sts=4 ts=4 et
        autocmd FileType zsh        setlocal sw=4 sts=4 ts=4 et
        autocmd FileType python     setlocal sw=4 sts=4 ts=4 et
        autocmd FileType scala      setlocal sw=4 sts=4 ts=4 et
        autocmd FileType json       setlocal sw=4 sts=4 ts=4 et
        autocmd FileType html       setlocal sw=2 sts=2 ts=2 et
        autocmd FileType css        setlocal sw=4 sts=4 ts=4 et
        autocmd FileType scss       setlocal sw=4 sts=4 ts=4 et
        autocmd FileType sass       setlocal sw=4 sts=4 ts=4 et
        autocmd FileType javascript setlocal sw=4 sts=4 ts=4 et
        autocmd FileType yaml       setlocal sw=2 sts=2 ts=2 et
    endif
    " > $VIMRC
    [[ ! -e $ROOT_VIMRC ]] && { sudo cp $VIMRC $ROOT_VIMRC; }
}

function redhat7_6_mount(){
    vimrc
    local device="/dev/nvme1n1"
    local target="/data"
    local fstab="/etc/fstab"

    FILESYSTEM=`sudo file -s ${device} | awk '{print $2}'`
    if [ $FILESYSTEM == "data" ]; then
        sudo mkfs -t xfs $device
        [[ ! -e $target ]] && { sudo mkdir $target; }
        sudo mount $device $target
    fi
    local uuid=`sudo blkid -o value -s UUID $device`
    local uuid="UUID="$uuid" "$target" xfs defaults,nofail 0 2"
    sudo cp /etc/fstab /etc/fstab_org
    sudo echo $uuid >> $fstab
    sudo umount $target
    sudo mount -a
    if [ "$(df -h | grep $device)" != "" ]; then
        echo "Completed."
    else
        echo "You didn't mount on properly."
    fi
}

function main(){
    redhat7_6_mount
}

main
