storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

ui = true
disable_mlock = true


auth "token" {
  default_lease_ttl = "0"
  max_lease_ttl     = "0"

  roles {
    role_name = "root"
    allowed_policies = "*"
  }
}

path "secret/data/database/postgres" {
  capabilities = ["read"]
}