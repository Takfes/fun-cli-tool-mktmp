## USAGE

- Make sure [gist url](https://gist.github.com/Takfes/f851ba72f994ec51c9bee09f1ba27417) is updated
- Create a function like so

```{bash}
mktmp() {
    curl -sSL https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/5d7965b9feb90b6bf8f63113704860e18c620a16/main.py | python - "$@"
}
```

- Call the function : `mktmp <foldername>`
