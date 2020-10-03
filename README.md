# Holly Settings

## Project goal

Holly Settings heavily borrows from `python-configuration` library and is inspired by it.

## Alternatives

| Library                           | Holly | Dynaconf |
| --------------------------------- | ----- | -------- |
| **Read from `.json`**             | x     | x        |
| **Read from `.toml`**             | x     | x        |
| **Read from `.ini`**              | x     | x        |
| **Read from env vars**            | x     | x        |
| **Read from `.py`**               |       | x        |
| **Read from `.env`**              |       | x        |
| **Read from dict object**         | x     |          |
| **Read from Redis**               |       | x        |
| **Read from Hashicorp Vault**     |       | x        |
| **Default values**                | x     | x        |         
| **Multienvironment**              |       | x        |
| **Attribute access**              | x     | x        |
| **Dotted key access**             | x     | x        |
| **Merging**                       | x     | onelevel |
| **Interpolation**                 |       | x        |
| **Saving**                        | x     | x        |
| **CLI**                           | x     | x        |
| **Printing**                      | x     | x        |
| **Validators**                    |       | x        |
| **Masking sensitive info**        |       | x        |
| **Django integration**            |       | x        |
| **Flask integration**             |       | x        |
| **Hot reload**                    |       |          |
| *Python 3.6*                      |       |          |
| *Python 3.7*                      |       |          |
| *Python 3.8*                      | x     |          |