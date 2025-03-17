# 1. Setup MySQL database

```
helm install xp-mysql oci://registry-1.docker.io/bitnamicharts/mysql
```

Execute the following to get the administrator credentials:

Bash

```
MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default xp-mysql -o jsonpath="{.data.mysql-root-password}" | base64 -d)
```

Powershell

```
$MYSQL_ROOT_PASSWORD = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String( (kubectl get secret --namespace default xp-mysql -o jsonpath="{.data.mysql-root-password}") ))
```

Run a pod that you can use as a client:

```
kubectl run xp-mysql-client --rm --tty -i --restart='Never' --image  docker.io/bitnami/mysql:8.4.4-debian-12-r4 --namespace default --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD --command -- bash
```

Connect to the MySQL pod. Fill in the $MYSQL_ROOT_PASSWORD part

```
mysql -h xp-mysql.default.svc.cluster.local -uroot -p"$MYSQL_ROOT_PASSWORD"

mysql -h xp-mysql.default.svc.cluster.local -uroot -p"Q4KWAcGsoD"
```

Create a user that will be the user to give to the JDBC. Note this is the user and password that will be set in dev-secrets.yaml.

```
CREATE USER 'appuser'@'%' IDENTIFIED BY 'mypassword1';
GRANT ALL PRIVILEGES ON my_database.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
```

```
SHOW DATABASES;

USE my_database;

CREATE TABLE Accounts (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(50) NOT NULL,
    DateOfBirth DATE,
    AccountNumber VARCHAR(20) UNIQUE,
    Balance DECIMAL(18, 2) DEFAULT 0.00,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Accounts (Email, DateOfBirth, AccountNumber, Balance)
VALUES 
('john.doe@example.com', '1985-06-15', 'ACC123456', 1000.00),
('jane.smith@example.com', '1990-09-25', 'ACC654321', 2500.50),
('alice.jones@example.com', '1978-12-05', 'ACC789012', 150.75);
```

```
{
  "query": "query { getAccounts { id email dateOfBirth accountNumber balance createdAt } }"
}
```

```
{
  "query": "query { users(limit: 2, skip: 0) { id name email } }"
}
```

```
{
  "query": "mutation CreateUser($name: String!, $email: String!) { createUser(name: $name, email: $email) { id name email } }",
  "variables": {
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```