import LDAP

getld = ldapInit "ldap.dartmouth.edu" ldapPort

ldapsearch l q = ldapSearch l (Just "dc=dartmouth,dc=edu") LdapScopeSubtree (Just q) LDAPAllUserAttrs False

getattrs attrs = map (filter (flip elem attrs) . leattrs)

--renameattrs
