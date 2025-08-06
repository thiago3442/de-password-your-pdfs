# de-password-your-pdfs

Utility to remove passwords from multiple PDF files.

## Uso

1. Coloque os PDFs protegidos na pasta `input/`.
2. Crie um arquivo `passwords.csv` no formato `nome_do_arquivo.pdf,senha`.
3. Execute o script para gerar os PDFs desbloqueados na pasta `output/`:

```bash
pip install -r requirements.txt
python unlock_pdfs.py input passwords.csv output
```

Use `--log-level` para ajustar a verbosidade dos logs (por exemplo, `DEBUG`).

Cada PDF desbloqueado será salvo com o sufixo `_unlocked.pdf`.
