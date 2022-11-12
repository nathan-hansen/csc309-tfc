table User {
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
  type varchar
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
  keywords TextField
  capacity IntegerField
  start_time DateTimeField
  // this could be end time instead
  duration DurationField 
}
Ref: Class.studio > Studio.id

table Subscription {
  id int [pk]
  payment DecimalField
  // one of "monthly", "yearly", etc
  // change if more complexity needed
  interval StringField
}

table Payment {
  id int [pk]
  user ForeignKey
  card_number IntegerField
  card_expiry IntegerField
  card_security IntegerField
  current_subscription ForeignKey
}
Ref: Payment.user > User.id
Ref: Payment.current_subscription > Subscription.id

table PaymentHistory {
  id int [pk]
  user ForeignKey
  timestamp DateTimeField
  amount DecimalField
  card_number IntegerField
  card_expiry IntegerField
  card_security IntegerField
}
Ref: PaymentHistory.user > User.id

