<a id="alternatives"></a>
## Alternative Libraries

Below is a primitive analysis of features of alternative libraries doing similar job.

| Library                           | **ilexconf** | dynaconf | python-configuration |
| --------------------------------- | ----- | -------- | -- |
| **Read from `.json`**             | x     | x        | x  |
| **Read from `.toml`**             | x     | x        | x  |
| **Read from `.ini`**              | x     | x        | x  |
| **Read from env vars**            | x     | x        | x  |
| **Read from `.py`**               |       | x        | x  |
| **Read from `.env`**              |       | x        | x  |
| **Read from dict object**         | x     |          | x  |
| **Read from Redis**               |       | x        |    |
| **Read from Hashicorp Vault**     |       | x        |    |
| **Default values**                | x     | x        |    |    
| **Multienvironment**              |       | x        |    |
| **Attribute access**              | x     | x        | x  |
| **Dotted key access**             | x     | x        | x  |
| **Merging**                       | x     | x        | x  |
| **Interpolation**                 |       | x        | x  |
| **Saving**                        | x     | x        |    |
| **CLI**                           | x     | x        |    |
| **Printing**                      | x     | x        |    |
| **Validators**                    |       | x        |    |
| **Masking sensitive info**        |       | x        | x  |
| **Django integration**            |       | x        |    |
| **Flask integration**             |       | x        |    |
| **Hot reload**                    |       |          |    |
| *Python 3.6*                      |       |          | x  |
| *Python 3.7*                      |       |          | x  |
| *Python 3.8*                      | x     |          | x  |
