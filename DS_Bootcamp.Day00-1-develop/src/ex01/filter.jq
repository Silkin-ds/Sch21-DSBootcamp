[
    "id",
    "created_at",
    "name",
    "has_test",
    "alternate_url"
  ],
  (.items[] | [
    .id,
    .created_at,
    .name,
    .has_test,
    .alternate_url
  ]) | @csv