# Vagrant-based setup

Virtual machine setup for the Airflow overview talk at DSEC given by Reinis Bekeris on 28th Seprwmvwe 2024

> **DONT USE IN PRODUCTION** This is for training, demo, etc. Learn how to secure it before you use it for anything other than that.

> Make sure your computer has 8G memory or more.

This relates to 
- [Reinis' DSEC talk](https://www.meetup.com/data-science-and-engineering-club/events/303120347/?eventOrigin=group_past_events)
- [dockerized airflow setup repo](https://github.com/rbekeris/Docker_Airflow_Postgres.git)

Gets you the airflow up & running and is imho the easiest way to do it.

1. Install virtualbox

> Use [7.0.*](https://www.virtualbox.org/wiki/Download_Old_Builds_7_0) version, the latest (7.1.*) are not supported by vagrant yet.

2. Install [vagrant](https://developer.hashicorp.com/vagrant/install?product_intent=vagrant#windows)

3. Clone this repo

4. Using terminal/cmd/powershell in the repo folder, do

The below commands will install the virtual machine and install docker inside it.

```sh
cd vagrant-setup
vagrant up
vagrant provision
vagrant ssh
```

> If `vagrant up` errors out complaining about CPU, you need to configure BIOS and enable virtualization in the CPU section.


Your command prompt should be showing `vagrant@ubuntu:~$`. You are now on the virtual machine.

### Use

- follow the rest of the tutorial from the main readme in this repo.
- when `docker compose` is up, you can access airflow UI from your laptop's btowser, just visit http://192.168.56.0:8080. The port is forwarded from the virtual machine to your machine, but it's kept isolated in a private network so that it can be accessed only from your laptop, but not by somebody sitting next to you in a cafe.

### Tidying

- to exit the virtual machine hit `ctr+d`
- to stop the virtual machine run `vagrant halt` from outside of it (your system cmd/powershell/terminal)
- to destroy the vm run `vagrant destroy` from outside of it (your system cmd/powershell/terminal)
