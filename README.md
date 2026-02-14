Up docker swarm with command:

```bash
export $(cat .env) > /dev/null 2>&1; docker stack deploy -c stack.yaml app
```
This command will setup environment for stack. Then create a stack called app.
