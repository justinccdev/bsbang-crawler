import logging


logger = logging.getLogger(__name__)


class BioschemasFilter:
    def __init__(self, config):
        self.config = config

    def filter(self, jsonlds):
        """
        Filters out non-bioschemas jsonld.

        FIXME: At some point in the future we may well be interested in ordinary schema.org

        :param jsonlds: [<jsonld>]
        :return: [<jsonld>]
        """

        final_jsonlds = []

        for jsonld in jsonlds:
            try:
                if '@type' not in jsonld:
                    logger.debug('Ignoring as no @type present')
                    continue

                schema = jsonld['@type']
                if schema not in self.config['schemas_to_parse']:
                    logger.debug('Ignoring as %s is not a schema we are configured to parse', schema)

                self._assert_mandatory_jsonld_properties(schema, jsonld)
                final_jsonlds.append(jsonld)
            except KeyError as err:
                logger.debug('Ignoring %s as %s', jsonld, err)
                continue

        return final_jsonlds

    def _assert_mandatory_jsonld_properties(self, schema, jsonld):
        # print('Asserting schema %s' % schema)
        """Assert that the properties we require for a schema, and its parent schemas, exists in the jsonld"""
        if schema in self.config['mandatory_properties']:
            for prop in self.config['mandatory_properties'][schema]:
                if prop not in jsonld:
                    raise KeyError('Mandatory property %s not present for type %s' % (prop, type))

        parent_schema = self.config['schema_inheritance_graph'][schema]
        if parent_schema is not None:
            self._assert_mandatory_jsonld_properties(parent_schema, jsonld)