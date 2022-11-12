table Account {
  id int [pk]
  first_name StringField
  last_name StringField
  email StringField
  avatar ImageField
  phone_number StringField
  
}

table Studio {
  id int [pk]
  name StringField
  address StringField
  latitude FloatField
  longitude FloatField
  postal_code StringField
  phone_number StringField
  // images
}

table StudioImage {
  studio ForeignKey
  image ImageField
}
Ref: StudioImage.studio > Studio.id

table Amenities {
  studio ForeignKey
  type StringField
  quantity int
}
Ref: Amenities.studio > Studio.id

table Class {
  id int [pk]
  studio ForeignKey
  name StringField
  description TextField
  coach StringField
  // keywords type could change...
  // assess during implementation
  duration DurationField
}
Ref: Class.studio > Studio.id

table Keywords {
  keyword StringField
  class ForeignKey
}
Ref: Keywords.class > Class.id

// Use this table if you want to cancel 
// one time in a recursive class
table ClassTimeTable {
  id int [pk]
  class ForeignKey
  time DateTimeField
  spotleft IntegerField
}
Ref: ClassTimeTable.class > Class.id

table Subscription {
  id int [pk]
  payment DecimalField
  // one of "monthly", "yearly", etc
  // change if more complexity needed
  interval StringField
}

table Payment {
  id int [pk]
  account ForeignKey
  card_number IntegerField
  card_expiry IntegerField
  card_security IntegerField
  current_subscription ForeignKey
}
Ref: Payment.account > Account.id
Ref: Payment.current_subscription > Subscription.id

table PaymentHistory {
  id int [pk]
  account ForeignKey
  timestamp DateTimeField
  amount DecimalField
  card_number IntegerField
  card_expiry IntegerField
  card_security IntegerField
}
Ref: PaymentHistory.account > Account.id

table EnrollClass {
  account ForeignKey
  classtime ForeignKey
}
Ref: EnrollClass.account > Account.id
Ref: EnrollClass.classtime > ClassTimeTable.id
