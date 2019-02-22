# OpenStack resources
- go to https://cl-gitlab.intra.codilime.com/
  select given project
  if possible go to settings, CI/CD, Runners, click Expand
  in section 'Setup a specific Runner manually' there is a registration token
  copy that token and paste it into `cloud-config.centos7.yaml` in gitlab-runner
  section just after `--registration-token`
- log in to https://stack.intra.codilime.com/project/ as
  Domain: Users
  Username: login like to FreeIPA/Wifi/VPN
  Password: login like to FreeIPA/Wifi/VPN
  notice - you must be assigned to the project to be able to log in
- switch project to `ADM-Luncher2`
- (optional) create network:
  name: 'private',
  CIDR: 10.10.11.0/24
  Gateway: 10.10.11.1
  enable DHCP:
    allocation pools: 10.10.11.11,10.10.11.99
    dns name servers: 10.5.88.20 (this is codlimime internal dns, needed later)
    host routes: leave empty
- create router:
  attached to public and 'private' network
  fixed IP: 10.10.11.1
- edit security groups:
  name: default
  allow: ingress 0.0.0.0/0
    SSH: 22/tcp
    cockpit: 9090/tcp
    deploy_review: 3000-30000/tcp (port range)
    deploy_stage: 80/tcp (or HTTP)
    ICMP: ~
- floating IP: assign one per instance, remember it.
- edit `cloud-config.centos7-shared.yaml`:
  add new user to users section with new public key and password for sudo
  ensure to set proper entries in gitlab-runner install section, especially:
  - name
  - registration token
- create instance:
  name: whatever you like
  disk: 32GB at least
  from image, select centos 7 qcow2
  delete disk on termination
  flavors: something like 2 cores, 4 gb ram, 16gb disk, for example m3.medium
  key pair: add key pair if needed, or update cloud-config.centos7-shared.yaml in users section by adding new user
  configuration -> customization script: copy/paste cloud-config.centos7-shared.yaml contents
- click launch, after that assign floating IP to new instance
- wait over 10 min until instance installs packages and runs cloud-init config.
- ssh via floating IP to instance and user added to cloud-config.centos7-shared.yaml
- verify that instance is connected to gitlab as worker - go to project,
  settings, CI/CD, runners and it should be there

# Known limitations
- no firewall on current setup (just security groups)
- need to test deployments under /srv
- auto parition mounts /dev/vdb under /mnt as ext4
