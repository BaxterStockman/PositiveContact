from google.appengine.ext import ndb


def valid_phone_number(prop, value, length):
    if(len(str(value)) == length):
        return value
    else:
        raise ValueError("{0} must be {1} digits long".format(prop, length))


valid_phone_number_3 = lambda prop, value: valid_phone_number(prop, value, 3)
valid_phone_number_4 = lambda prop, value: valid_phone_number(prop, value, 4)


# Thanks to https://developers.google.com/appengine/docs/python/ndb/properties
# for ideas about nested models
class Address(ndb.Model):
    type = ndb.StringProperty()
    number = ndb.IntegerProperty()
    street = ndb.StringProperty()
    city = ndb.StringProperty()


class PhoneNumber(ndb.Model):
    type = ndb.StringProperty()
    area_code = ndb.IntegerProperty(validator=valid_phone_number_3)
    prefix = ndb.IntegerProperty(validator=valid_phone_number_3)
    line_number = ndb.IntegerProperty(validator=valid_phone_number_4)
    full_number = ndb.ComputedProperty(lambda self:
                                       "{0}-{1}-{2}".format(self.area_code,
                                                            self.prefix,
                                                            self.line_number))


class Email(ndb.Model):
    user_name = ndb.StringProperty(indexed=False)
    domain_name = ndb.StringProperty(indexed=False)
    tld = ndb.StringProperty(indexed=False)
    full_email = ndb.ComputedProperty(lambda self:
                                      "{0}@{1}.{2}".format(self.user_name,
                                                           self.domain_name,
                                                           self.tld),
                                      indexed=True)


class Contact(ndb.Model):
    fname = ndb.StringProperty()
    lname = ndb.StringProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)
    phone_numbers = ndb.StructuredProperty(PhoneNumber, repeated=True)
    email_addresses = ndb.StructuredProperty(Email, repeated=True)
    updated = ndb.DateTimeProperty(auto_now=True)
