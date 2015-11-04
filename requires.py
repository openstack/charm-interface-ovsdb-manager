from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class OVSDBManagerRequires(RelationBase):
    scope = scopes.GLOBAL
    auto_accessors = ['protocol', 'private-address', 'host', 'port']

    @hook('{requires:ovsdb-manager}-relation-{joined,changed,departed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection_string():
            self.set_state('{relation_name}.access.available')
        else:
            self.remove_state('{relation_name}.access.available')

    @hook('{requires:ovsdb-manager}-relation-broken')
    def broken(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.access.available')

    def connection_string(self):
        """Open vSwitch connection string

        Returns the connection string to use for Open vSwitch or None
        if the remote ODL controller has not presented this data
        yet.
        """
        data = {
            'host': self.host() or self.private_address(),
            'port': self.port() or '6640',
            'protocol': self.protocol(),
        }
        if all(data.values()):
            return "{protocol}:{host}:{port}".format(**data)
        else:
            return None
