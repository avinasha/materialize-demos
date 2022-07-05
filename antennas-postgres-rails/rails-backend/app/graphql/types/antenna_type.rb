# frozen_string_literal: true

module Types
  class AntennaType < Types::BaseObject
    field :antenna_id, String
    field :geojson, String
    field :performance, Float
    field :diff, Integer
    field :timestamp, Float
  end
end
