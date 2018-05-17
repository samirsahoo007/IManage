from django.conf import settings
　
import ldap
import logging
import time
　
　
class Search:
　
    def ldapsearch(self, searchterm, ctr=0):
        if ctr is None:
            ctr = 0
　
        limit = 10
　
        logger = logging.getLogger('django.request')
        try:
            l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
　
            l.bind_s(settings.AD_BIND_DN, settings.AD_BIND_PASS, ldap.AUTH_SIMPLE)
　
            l.protocol_version = ldap.VERSION3
        except ldap.LDAPError, e:
            l.unbind_s()
            logger.error("Exception with LDAP1: " + e.message)
            if ctr < limit:
                ctr = ctr + 1
                time.sleep(2)
                logger.error("Retrying: " + str(ctr))
                return self.ldapsearch(searchterm, ctr)
            else:
                raise Exception("Ldap Failure, exceeded retries.")
　
        baseDN = settings.LDAPSEARCH_BASE_DN
        searchScope = ldap.SCOPE_SUBTREE
        ## retrieve all attributes - again adjust to your needs - see documentation for more options
        retrieveAttributes = None
        searchFilter = searchterm   # settings.LDAPSEARCH_FILTER
        #  logger.error("Search Filter: " + searchFilter)
        result_set = []
　
        try:
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    ## here you don't have to append to a list
                    ## you could do whatever you want with the individual entry
                    ## The appending to list is just for illustration.
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
　
        except ldap.LDAPError, e:
            l.unbind_s()
            logger.error("Exception with LDAP: ")
            logger.error(e.message)
            if ctr < limit:
                ctr = ctr + 1
                logger.error("Retrying: " + str(ctr))
                return self.ldapsearch(searchterm, ctr)
            else:
                raise Exception("Ldap Failure, exceeded retries.")
　
        l.unbind_s()
　
        return result_set
