#!/usr/bin/env bash

login=${1:-admin}
email=${2:-admin@luncher.com}
password=${3:-luncher123}

RealPath()
{
    pushd "$1" &> /dev/null
    pwd
    popd &> /dev/null
}

ThisDir=$(RealPath "$(dirname "$0")")

echo "from luncher.users.models import User; User.objects.create_superuser('$login', '$email', '$password')" | "$ThisDir/../.venv/bin/python" "$ThisDir/../manage.py" shell
